"""
Task 1: Session Storage Tests
Tests that /login creates a session and /me retrieves the user.
"""

from fastapi.testclient import TestClient
from app import app, r

client = TestClient(app)


def test_login_returns_session_id():
    response = client.post("/login", json={"user_id": "alice"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["session_id"]) > 0


def test_me_returns_user_id():
    login_resp = client.post("/login", json={"user_id": "alice"})
    session_id = login_resp.json()["session_id"]

    response = client.get("/me", headers={"X-Session-Id": session_id})
    assert response.status_code == 200
    assert response.json()["user_id"] == "alice"


def test_invalid_session_returns_401():
    response = client.get("/me", headers={"X-Session-Id": "nonexistent"})
    assert response.status_code == 401


def test_session_has_ttl():
    login_resp = client.post("/login", json={"user_id": "alice"})
    session_id = login_resp.json()["session_id"]

    ttl = r.ttl(f"session:{session_id}")
    assert 0 < ttl <= 3600


def test_different_users_get_different_sessions():
    resp1 = client.post("/login", json={"user_id": "alice"})
    resp2 = client.post("/login", json={"user_id": "bob"})

    sid1 = resp1.json()["session_id"]
    sid2 = resp2.json()["session_id"]
    assert sid1 != sid2

    me1 = client.get("/me", headers={"X-Session-Id": sid1})
    me2 = client.get("/me", headers={"X-Session-Id": sid2})
    assert me1.json()["user_id"] == "alice"
    assert me2.json()["user_id"] == "bob"
