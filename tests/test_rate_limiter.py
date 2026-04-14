"""
Task 2: Rate Limiter Tests
Tests that /request enforces a limit of 5 requests per 60-second window.
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_allows_requests_under_limit():
    for _ in range(5):
        response = client.get("/request?user_id=test_user")
        assert response.status_code == 200


def test_blocks_sixth_request():
    for _ in range(5):
        client.get("/request?user_id=test_user")

    response = client.get("/request?user_id=test_user")
    assert response.status_code == 429


def test_different_users_have_separate_limits():
    # Exhaust user_a's limit
    for _ in range(5):
        client.get("/request?user_id=user_a")

    # user_b should still be allowed
    response = client.get("/request?user_id=user_b")
    assert response.status_code == 200


def test_returns_remaining_count():
    response = client.get("/request?user_id=test_user")
    data = response.json()
    assert "remaining" in data
    assert data["remaining"] == 4  # 5 max - 1 used


def test_remaining_decreases():
    for i in range(5):
        response = client.get("/request?user_id=test_user")
        data = response.json()
        assert data["remaining"] == 4 - i
