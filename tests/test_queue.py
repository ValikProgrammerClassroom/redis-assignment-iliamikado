"""
Task 3: Task Queue Tests
Tests that /task (POST and GET) implements a FIFO queue.
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_add_task():
    response = client.post("/task", json={"task": "send_email"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"


def test_get_task():
    client.post("/task", json={"task": "send_email"})
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json()["task"] == "send_email"


def test_fifo_order():
    client.post("/task", json={"task": "first"})
    client.post("/task", json={"task": "second"})
    client.post("/task", json={"task": "third"})

    assert client.get("/task").json()["task"] == "first"
    assert client.get("/task").json()["task"] == "second"
    assert client.get("/task").json()["task"] == "third"


def test_empty_queue_returns_404():
    response = client.get("/task")
    assert response.status_code == 404


def test_queue_length():
    client.post("/task", json={"task": "task_1"})
    response = client.post("/task", json={"task": "task_2"})
    assert response.json()["queue_length"] == 2
