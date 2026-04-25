"""
JARVIS v2 — Iteration 2 backend tests
Covers: auth, SSE streaming, voice (STT/TTS), export, multi-turn context.

Real LLM/Whisper/TTS calls are made — keep counts modest.
"""
import io
import json
import math
import os
import struct
import wave
import uuid

import httpx
import pymongo
import pytest
import requests
from datetime import datetime, timedelta, timezone

_mongo = pymongo.MongoClient("mongodb://localhost:27017")["jarvis_db"]


# ---------- url & seeded creds (from review_request) ---------------------
def _read_url():
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("REACT_APP_BACKEND_URL missing")


BASE_URL = _read_url().rstrip("/")
API = f"{BASE_URL}/api"

SEED_USER_A = {
    "user_id": "user_cb59d95cccf9",
    "session_token": "test_jarvis_1777130060331",
    "email": "jarvis.tester@example.com",
}


# ---------- helpers ------------------------------------------------------
@pytest.fixture(scope="session")
def auth_headers():
    return {"Authorization": f"Bearer {SEED_USER_A['session_token']}"}


@pytest.fixture(scope="session")
def http(auth_headers):
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", **auth_headers})
    return s


@pytest.fixture(scope="session")
def anon():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---------- AUTH ---------------------------------------------------------
class TestAuth:
    def test_session_missing_header_returns_400(self, anon):
        r = anon.post(f"{API}/auth/session")
        assert r.status_code == 400

    def test_session_invalid_id_returns_401(self, anon):
        r = anon.post(f"{API}/auth/session",
                      headers={"X-Session-ID": "definitely-not-real-xyz"})
        assert r.status_code == 401

    def test_me_unauth_returns_401(self, anon):
        r = anon.get(f"{API}/auth/me")
        assert r.status_code == 401

    def test_me_with_bearer_returns_user(self, http):
        r = http.get(f"{API}/auth/me")
        assert r.status_code == 200
        data = r.json()
        assert data["user_id"] == SEED_USER_A["user_id"]
        assert data["email"] == SEED_USER_A["email"]
        assert data["name"]


# ---------- USER-SCOPED SESSIONS -----------------------------------------
@pytest.fixture(scope="module")
def user_a_session(http):
    """Create a chat session under user A and return its id."""
    r = http.post(f"{API}/chat", json={"message": "ping for scoping"}, timeout=120)
    assert r.status_code == 200, r.text
    sid = r.json()["session_id"]
    yield sid
    try:
        http.delete(f"{API}/sessions/{sid}", timeout=20)
    except Exception:
        pass


@pytest.fixture(scope="module")
def user_b_token():
    """Insert a second user via pymongo and return its bearer token."""
    token = f"test_session_userB_{uuid.uuid4().hex[:8]}"
    uid = f"user_{uuid.uuid4().hex[:12]}"
    _mongo["users"].insert_one({
        "user_id": uid, "email": f"userB.{uid}@example.com",
        "name": "User B", "created_at": datetime.now(timezone.utc),
    })
    _mongo["user_sessions"].insert_one({
        "user_id": uid, "session_token": token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc),
    })
    yield {"token": token, "user_id": uid}
    _mongo["user_sessions"].delete_many({"session_token": token})
    _mongo["users"].delete_many({"user_id": uid})
    _mongo["sessions"].delete_many({"user_id": uid})


class TestUserScoping:
    def test_user_b_cannot_read_user_a_messages(self, user_a_session, user_b_token):
        r = requests.get(
            f"{API}/sessions/{user_a_session}/messages",
            headers={"Authorization": f"Bearer {user_b_token['token']}"},
            timeout=20,
        )
        assert r.status_code == 403, r.text

    def test_user_b_cannot_delete_user_a_session(self, user_a_session, user_b_token):
        r = requests.delete(
            f"{API}/sessions/{user_a_session}",
            headers={"Authorization": f"Bearer {user_b_token['token']}"},
            timeout=20,
        )
        assert r.status_code == 403

    def test_user_a_session_not_in_user_b_list(self, user_a_session, user_b_token):
        r = requests.get(
            f"{API}/sessions",
            headers={"Authorization": f"Bearer {user_b_token['token']}"},
            timeout=20,
        )
        assert r.status_code == 200
        assert all(s["id"] != user_a_session for s in r.json())


# ---------- STATUS -------------------------------------------------------
def test_status_voice_online(anon):
    r = anon.get(f"{API}/status")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 5
    voice = next(i for i in items if i["name"] == "voice")
    assert voice["status"] == "online"


def test_health(anon):
    r = anon.get(f"{API}/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


# ---------- CHAT (auth + anon) -------------------------------------------
def test_chat_authed_attaches_to_user(http):
    r = http.post(f"{API}/chat", json={"message": "hello jarvis"}, timeout=120)
    assert r.status_code == 200
    sid = r.json()["session_id"]
    sessions = http.get(f"{API}/sessions").json()
    assert any(s["id"] == sid for s in sessions)
    http.delete(f"{API}/sessions/{sid}")


def test_chat_anonymous_still_works(anon):
    r = anon.post(f"{API}/chat", json={"message": "hi"}, timeout=120)
    assert r.status_code == 200
    sid = r.json()["session_id"]
    # cleanup
    anon.delete(f"{API}/sessions/{sid}")


# ---------- SSE STREAMING ------------------------------------------------
def _parse_sse(body: str):
    """Yield (event, data_obj) pairs from a raw SSE response body."""
    blocks = body.strip().split("\n\n")
    for block in blocks:
        ev, data = None, None
        for line in block.splitlines():
            if line.startswith("event:"):
                ev = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                data = line.split(":", 1)[1].strip()
        if ev and data is not None:
            try:
                yield ev, json.loads(data)
            except Exception:
                yield ev, data


class TestStreaming:
    def test_stream_emits_meta_chunks_done_and_persists(self, auth_headers):
        events = []
        with httpx.Client(timeout=180) as client:
            with client.stream(
                "POST",
                f"{API}/chat/stream",
                json={"message": "say hi briefly"},
                headers={**auth_headers, "Content-Type": "application/json"},
            ) as r:
                assert r.status_code == 200
                ctype = r.headers.get("content-type", "")
                assert "text/event-stream" in ctype, ctype
                body = b""
                for chunk in r.iter_bytes():
                    body += chunk
        parsed = list(_parse_sse(body.decode()))
        evs = [e for e, _ in parsed]
        assert "meta" in evs, evs
        assert any(e == "chunk" for e in evs), evs
        assert evs[-1] == "done", evs

        meta = next(d for e, d in parsed if e == "meta")
        assert "session_id" in meta and "category" in meta and "title" in meta
        assert meta["category"] in {"research", "coding", "build", "content", "general"}

        done = next(d for e, d in parsed if e == "done")
        jm = done["jarvis_message"]
        sid = meta["session_id"]
        assert jm["session_id"] == sid

        # persistence — fetch via GET
        r = requests.get(
            f"{API}/sessions/{sid}/messages",
            headers=auth_headers,
            timeout=20,
        )
        assert r.status_code == 200
        msgs = r.json()
        assert any(m["id"] == jm["id"] for m in msgs)
        assert any(m["role"] == "jarvis" for m in msgs)

        # cleanup
        requests.delete(f"{API}/sessions/{sid}", headers=auth_headers)


# ---------- MULTI-TURN CONTEXT -------------------------------------------
def test_multi_turn_context(http):
    r1 = http.post(f"{API}/chat",
                   json={"message": "Remember the codeword: TANGERINE-42."},
                   timeout=120)
    assert r1.status_code == 200
    sid = r1.json()["session_id"]
    r2 = http.post(f"{API}/chat",
                   json={"session_id": sid,
                         "message": "What was the codeword I just gave you? Reply with only the codeword."},
                   timeout=120)
    assert r2.status_code == 200
    reply = r2.json()["jarvis_message"]["content"]
    assert "TANGERINE" in reply.upper(), f"context lost. reply={reply!r}"
    http.delete(f"{API}/sessions/{sid}")


# ---------- VOICE — TTS --------------------------------------------------
class TestTTS:
    def test_tts_returns_audio(self, http):
        r = http.post(f"{API}/voice/tts", json={"text": "hello"}, timeout=60)
        assert r.status_code == 200
        assert r.headers.get("content-type", "").startswith("audio/mpeg")
        assert len(r.content) > 200  # non-empty mp3

    def test_tts_empty_text_400(self, http):
        r = http.post(f"{API}/voice/tts", json={"text": "  "}, timeout=20)
        assert r.status_code == 400

    def test_tts_oversized_truncated_ok(self, http):
        r = http.post(f"{API}/voice/tts",
                      json={"text": "abc " * 1500}, timeout=120)  # >4000 chars
        assert r.status_code == 200
        assert r.headers.get("content-type", "").startswith("audio/mpeg")


# ---------- VOICE — STT --------------------------------------------------
def _make_wav_bytes(seconds=1.0, freq=440, rate=16000):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        n = int(seconds * rate)
        frames = bytearray()
        for i in range(n):
            sample = int(0.3 * 32767 * math.sin(2 * math.pi * freq * i / rate))
            frames += struct.pack("<h", sample)
        w.writeframes(bytes(frames))
    return buf.getvalue()


class TestSTT:
    def test_stt_empty_returns_400(self):
        files = {"audio": ("empty.wav", b"", "audio/wav")}
        r = requests.post(f"{API}/voice/transcribe", files=files, timeout=30)
        assert r.status_code == 400

    def test_stt_with_tone_returns_text_field(self):
        wav = _make_wav_bytes(seconds=1.0)
        files = {"audio": ("tone.wav", wav, "audio/wav")}
        r = requests.post(f"{API}/voice/transcribe", files=files, timeout=120)
        # whisper may return empty text on a pure tone — still must be 200 with key
        assert r.status_code == 200, r.text
        data = r.json()
        assert "text" in data and isinstance(data["text"], str)


# ---------- EXPORT -------------------------------------------------------
class TestExport:
    @pytest.fixture(scope="class")
    def export_session(self, auth_headers):
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json", **auth_headers})
        r = s.post(f"{API}/chat", json={"message": "export-me"}, timeout=120)
        sid = r.json()["session_id"]
        yield s, sid
        s.delete(f"{API}/sessions/{sid}")

    def test_export_md(self, export_session):
        s, sid = export_session
        r = s.get(f"{API}/sessions/{sid}/export?format=md", timeout=30)
        assert r.status_code == 200
        assert "text/markdown" in r.headers.get("content-type", "")
        assert "attachment" in r.headers.get("content-disposition", "").lower()
        assert ".md" in r.headers.get("content-disposition", "")
        assert "JARVIS" in r.text

    def test_export_json(self, export_session):
        s, sid = export_session
        r = s.get(f"{API}/sessions/{sid}/export?format=json", timeout=30)
        assert r.status_code == 200
        assert "application/json" in r.headers.get("content-type", "")
        body = r.json()
        assert "session" in body and "messages" in body
        assert body["session"]["id"] == sid

    def test_export_invalid_format_422(self, export_session):
        s, sid = export_session
        r = s.get(f"{API}/sessions/{sid}/export?format=xml", timeout=20)
        assert r.status_code == 422


# ---------- LOGOUT (last — invalidates a token) --------------------------
def test_logout_via_temp_user():
    """Insert a temp user/session, call logout via cookie, verify deleted."""
    token = f"test_logout_{uuid.uuid4().hex[:8]}"
    uid = f"user_{uuid.uuid4().hex[:12]}"
    _mongo["users"].insert_one({
        "user_id": uid, "email": f"logout.{uid}@example.com",
        "name": "Logout User", "created_at": datetime.now(timezone.utc),
    })
    _mongo["user_sessions"].insert_one({
        "user_id": uid, "session_token": token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc),
    })
    try:
        r = requests.post(f"{API}/auth/logout", cookies={"session_token": token}, timeout=20)
        assert r.status_code == 200 and r.json().get("ok") is True
        r2 = requests.get(f"{API}/auth/me",
                          headers={"Authorization": f"Bearer {token}"}, timeout=20)
        assert r2.status_code == 401
    finally:
        _mongo["users"].delete_many({"user_id": uid})
        _mongo["user_sessions"].delete_many({"session_token": token})
