"""JARVIS API end-to-end tests against the public REACT_APP_BACKEND_URL."""
import os
import time
import pytest
import requests

# The frontend .env file holds the public URL; back end is reachable through /api there.
def _read_frontend_url():
    path = "/app/frontend/.env"
    with open(path) as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("REACT_APP_BACKEND_URL not found")

BASE_URL = _read_frontend_url().rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---- health & status -----------------------------------------------------
def test_health(http):
    r = http.get(f"{API}/health", timeout=20)
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert data.get("mongo") is True


def test_status(http):
    r = http.get(f"{API}/status", timeout=20)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 5
    names = {d["name"] for d in data}
    assert names == {"router", "memory", "knowledge", "voice", "network"}
    for d in data:
        assert d["status"] in {"online", "standby", "offline"}
        assert d["label"] and d["detail"]


# ---- chat creates session and persists ----------------------------------
@pytest.fixture(scope="module")
def created_session(http):
    """Create a session via /api/chat and return (session_id, jarvis_msg)."""
    r = http.post(f"{API}/chat", json={"message": "hello"}, timeout=90)
    assert r.status_code == 200, r.text
    data = r.json()
    sid = data["session_id"]
    yield sid, data
    # cleanup
    try:
        http.delete(f"{API}/sessions/{sid}", timeout=20)
    except Exception:
        pass


def test_chat_creates_session(created_session):
    sid, data = created_session
    assert isinstance(sid, str) and len(sid) > 0
    jm = data["jarvis_message"]
    assert jm["role"] == "jarvis"
    assert jm["category"] in {"research", "coding", "build", "content", "general"}
    assert jm["content"].strip() != ""
    um = data["user_message"]
    assert um["role"] == "user" and um["content"] == "hello"


def test_sessions_list_contains_created(http, created_session):
    sid, _ = created_session
    r = http.get(f"{API}/sessions", timeout=20)
    assert r.status_code == 200
    items = r.json()
    assert any(s["id"] == sid for s in items)
    # sorted by updated_at desc
    if len(items) >= 2:
        assert items[0]["updated_at"] >= items[1]["updated_at"]


def test_messages_chronological(http, created_session):
    sid, _ = created_session
    r = http.get(f"{API}/sessions/{sid}/messages", timeout=20)
    assert r.status_code == 200
    msgs = r.json()
    assert len(msgs) >= 2
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "jarvis"
    assert msgs[0]["created_at"] <= msgs[1]["created_at"]


def test_chat_appends_to_existing_session(http, created_session):
    sid, _ = created_session
    r = http.post(f"{API}/chat", json={"session_id": sid, "message": "and now what?"}, timeout=90)
    assert r.status_code == 200
    assert r.json()["session_id"] == sid
    # message_count must have incremented
    sessions = http.get(f"{API}/sessions", timeout=20).json()
    matched = [s for s in sessions if s["id"] == sid][0]
    assert matched["message_count"] >= 4


# ---- routing accuracy (single representative request per category) -------
ROUTING_CASES = [
    ("research the AI agent market 2026 and give a concise overview of leaders", "research"),
    ("write a python rate limiter using a token bucket", "coding"),
    ("build a saas dashboard with auth, billing, and an admin panel", "build"),
    ("draft a tweet thread for our product launch tomorrow", "content"),
    ("hello", "general"),
]


@pytest.mark.parametrize("prompt,expected", ROUTING_CASES)
def test_routing_accuracy(http, prompt, expected):
    r = http.post(f"{API}/chat", json={"message": prompt}, timeout=120)
    assert r.status_code == 200, r.text
    data = r.json()
    cat = data["jarvis_message"]["category"]
    sid = data["session_id"]
    # cleanup
    try:
        http.delete(f"{API}/sessions/{sid}", timeout=20)
    except Exception:
        pass
    assert cat == expected, f"prompt='{prompt}' got category={cat}, expected {expected}"


# ---- delete -------------------------------------------------------------
def test_delete_session_removes_messages(http):
    r = http.post(f"{API}/chat", json={"message": "temp session for delete"}, timeout=90)
    assert r.status_code == 200
    sid = r.json()["session_id"]

    d = http.delete(f"{API}/sessions/{sid}", timeout=20)
    assert d.status_code == 200
    assert d.json().get("deleted") == sid

    # session no longer in list
    sessions = http.get(f"{API}/sessions", timeout=20).json()
    assert all(s["id"] != sid for s in sessions)

    # messages empty
    msgs = http.get(f"{API}/sessions/{sid}/messages", timeout=20).json()
    assert msgs == []


# ---- validation ---------------------------------------------------------
def test_chat_empty_message_returns_400(http):
    r = http.post(f"{API}/chat", json={"message": "   "}, timeout=20)
    assert r.status_code == 400
