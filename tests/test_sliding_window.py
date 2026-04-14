"""
Bonus: Sliding Window Rate Limiter Tests
Tests that /request_sliding enforces a rolling 60-second window.
Skipped automatically if the endpoint is not implemented.
"""

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def _is_implemented():
    """Return True if the endpoint looks implemented (not just `pass`)."""
    resp = client.get("/request_sliding?user_id=probe")
    # `pass` returns null/None body with 200; unimplemented = 501
    if resp.status_code == 501:
        return False
    if resp.status_code == 200 and resp.json() is None:
        return False
    return True


pytestmark = pytest.mark.skipif(
    not _is_implemented(),
    reason="Bonus: /request_sliding not implemented yet",
)


def test_allows_requests_under_limit():
    for _ in range(5):
        response = client.get("/request_sliding?user_id=test_user")
        assert response.status_code == 200


def test_blocks_sixth_request():
    for _ in range(5):
        client.get("/request_sliding?user_id=test_user")

    response = client.get("/request_sliding?user_id=test_user")
    assert response.status_code == 429


def test_different_users_have_separate_limits():
    for _ in range(5):
        client.get("/request_sliding?user_id=user_a")

    response = client.get("/request_sliding?user_id=user_b")
    assert response.status_code == 200


def test_returns_remaining_count():
    response = client.get("/request_sliding?user_id=test_user")
    data = response.json()
    assert "remaining" in data
    assert data["remaining"] == 4
