"""
JARVIS Iteration 3 — backend tests for LLM-provider toggle + PWA assets.
Plus ~5 quick regression checks.

Real LLM call cost is kept low (1 chat round-trip).
"""
import os
import re

import pytest
import requests


def _read_url():
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("REACT_APP_BACKEND_URL missing")


BASE_URL = _read_url().rstrip("/")
API = f"{BASE_URL}/api"
SEED_TOKEN = "test_jarvis_1777130060331"
AUTH = {"Authorization": f"Bearer {SEED_TOKEN}"}


# ---------- Provider toggle ---------------------------------------------
class TestLLMProvider:
    """Run sequentially via fixture order so we always restore emergent at end."""

    def test_get_default_emergent(self):
        r = requests.get(f"{API}/llm/provider", timeout=15)
        assert r.status_code == 200, r.text
        d = r.json()
        # may already be ollama from a previous test run — reset first
        if d["provider"] != "emergent":
            requests.post(f"{API}/llm/provider", json={"provider": "emergent"}, timeout=10)
            d = requests.get(f"{API}/llm/provider", timeout=15).json()
        assert d["provider"] == "emergent"
        assert d["healthy"] is True
        assert d["model"]
        assert "ollama_url" in d and "ollama_model" in d

    def test_switch_to_ollama_unhealthy(self):
        r = requests.post(f"{API}/llm/provider", json={"provider": "ollama"}, timeout=15)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["provider"] == "ollama"
        assert d["healthy"] is False  # no Ollama server in CI
        # GET reflects it
        r2 = requests.get(f"{API}/llm/provider", timeout=15).json()
        assert r2["provider"] == "ollama"

    def test_invalid_provider_400(self):
        r = requests.post(f"{API}/llm/provider", json={"provider": "invalid"}, timeout=10)
        assert r.status_code in (400, 422), r.text  # 422 if pydantic rejects, 400 if app rejects

    def test_restore_emergent_healthy(self):
        r = requests.post(f"{API}/llm/provider", json={"provider": "emergent"}, timeout=15)
        assert r.status_code == 200
        d = r.json()
        assert d["provider"] == "emergent"
        assert d["healthy"] is True

    def test_chat_round_trip_after_restore(self):
        r = requests.post(
            f"{API}/chat",
            json={"message": "Reply with exactly: OK"},
            headers={**AUTH, "Content-Type": "application/json"},
            timeout=120,
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert "session_id" in body and "jarvis_message" in body
        jm = body["jarvis_message"]
        assert jm.get("category") in {"research", "coding", "build", "content", "general"}
        assert isinstance(jm.get("content"), str) and len(jm["content"]) > 0
        # cleanup
        requests.delete(f"{API}/sessions/{body['session_id']}", headers=AUTH, timeout=20)


# ---------- PWA assets ---------------------------------------------------
class TestPWAAssets:
    def test_manifest(self):
        r = requests.get(f"{BASE_URL}/manifest.webmanifest", timeout=15)
        assert r.status_code == 200, r.text
        m = r.json()
        assert m["name"].startswith("JARVIS")
        assert m["start_url"] == "/"
        assert m["display"] == "standalone"
        assert isinstance(m.get("icons"), list) and len(m["icons"]) >= 2

    def test_service_worker(self):
        r = requests.get(f"{BASE_URL}/service-worker.js", timeout=15)
        assert r.status_code == 200
        assert "caches.open" in r.text

    def test_icons(self):
        for path in ("/icon-192.png", "/icon-512.png"):
            r = requests.get(f"{BASE_URL}{path}", timeout=15)
            assert r.status_code == 200, path
            assert r.headers.get("content-type", "").startswith("image/png")
            assert len(r.content) > 200

    def test_porcupine_params(self):
        r = requests.get(f"{BASE_URL}/porcupine_params.pv", timeout=30)
        assert r.status_code == 200
        size = len(r.content)
        assert size >= 900_000, f"size={size}"

    def test_index_links_pwa(self):
        r = requests.get(f"{BASE_URL}/", timeout=15)
        assert r.status_code == 200
        html = r.text
        assert "/manifest.webmanifest" in html
        assert "/service-worker.js" in html


# ---------- Regression smoke (5 quick checks) ---------------------------
class TestRegression:
    def test_health(self):
        r = requests.get(f"{API}/health", timeout=10)
        assert r.status_code == 200 and r.json()["status"] == "ok"

    def test_root_version_2_1_0(self):
        r = requests.get(f"{API}/", timeout=10)
        assert r.status_code == 200
        assert r.json().get("version") == "2.1.0"

    def test_status(self):
        r = requests.get(f"{API}/status", timeout=10)
        assert r.status_code == 200
        assert len(r.json()) >= 4

    def test_auth_me(self):
        r = requests.get(f"{API}/auth/me", headers=AUTH, timeout=10)
        assert r.status_code == 200
        assert r.json()["email"] == "jarvis.tester@example.com"

    def test_sessions_list(self):
        r = requests.get(f"{API}/sessions", headers=AUTH, timeout=15)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
