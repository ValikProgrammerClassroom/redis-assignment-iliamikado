# Redis Assignments

Build a **FastAPI server** backed by Redis implementing three core backend patterns:
session storage, rate limiting, and task queues.

All your code goes in **`app.py`**. Each endpoint has `# TODO` comments explaining
what to implement and which Redis commands to use.

---

## Setup

### Prerequisites

- Python 3.10+
- Docker (for Redis)

### 1. Start Redis

```bash
docker-compose up -d
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server (for manual testing)

```bash
uvicorn app:app --reload
```

### 4. Run all tests

```bash
pytest tests/ -v
```

---

## Tasks

### Task 1: Session Storage

Implement user session management using Redis key-value pairs with TTL.

**Endpoints:**

| Method | Path       | Description                          |
|--------|------------|--------------------------------------|
| POST   | `/login`   | Create a session (body: `{"user_id": "alice"}`) |
| GET    | `/me`      | Get user from session (header: `X-Session-Id`)  |

**Redis commands you will need:**

```
SET session:<session_id> <user_id> EX 3600
GET session:<session_id>
```

**Run tests:** `pytest tests/test_session.py -v`

---

### Task 2: Rate Limiter (Fixed Window)

Implement API rate limiting: maximum **5 requests per 60 seconds** per user.

**Endpoint:**

| Method | Path                    | Description                |
|--------|-------------------------|----------------------------|
| GET    | `/request?user_id=<id>` | Rate-limited endpoint      |

**Responses:**
- `200 OK` with `{"status": "ok", "remaining": N}`
- `429 Too Many Requests` with `{"error": "rate limit exceeded"}`

**Redis commands you will need:**

```
INCR requests:user:<user_id>
EXPIRE requests:user:<user_id> 60
```

**Run tests:** `pytest tests/test_rate_limiter.py -v`

---

### Task 3: Task Queue (FIFO)

Implement a simple first-in-first-out task queue using Redis lists.

**Endpoints:**

| Method | Path    | Description                          |
|--------|---------|--------------------------------------|
| POST   | `/task` | Add a task (body: `{"task": "..."}`) |
| GET    | `/task` | Pop next task from queue             |

**Responses:**
- POST: `{"status": "queued", "queue_length": N}`
- GET (success): `{"task": "..."}`
- GET (empty): `404` with `{"error": "queue is empty"}`

**Redis commands you will need:**

```
LPUSH task_queue <task>
RPOP task_queue
LLEN task_queue
```

**Run tests:** `pytest tests/test_queue.py -v`

---

## Bonus Challenge

Implement a **sliding window rate limiter** using Redis Sorted Sets.

The fixed window approach has a flaw: a user can send 5 requests at second 59
and 5 more at second 61, effectively making 10 requests in 2 seconds.

A sliding window counts requests within a rolling 60-second window:

```
ZADD requests:user:<id> <timestamp> <unique_request_id>
ZREMRANGEBYSCORE requests:user:<id> 0 <now - 60>
ZCARD requests:user:<id>
```

---


## Useful Resources

- [Redis Commands Reference](https://redis.io/commands)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
