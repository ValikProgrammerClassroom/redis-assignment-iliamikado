"""
Implement the TODO sections below using Redis commands.
Each endpoint corresponds to one graded task.

Run locally:
    uvicorn app:app --reload

Run tests:
    pytest tests/ -v
"""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import redis
import uuid

app = FastAPI(title="Redis Assignments")

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

class LoginRequest(BaseModel):
    user_id: str

class TaskRequest(BaseModel):
    task: str


# ============================================================
# Task 1: Session Storage
# ============================================================
#
# POST /login
#   - Accept JSON body: {"user_id": "alice"}
#   - Generate a unique session_id (use uuid.uuid4())
#   - Store in Redis:  SET session:<session_id> <user_id> EX 3600
#   - Return JSON:     {"session_id": "<session_id>"}
#
# GET /me
#   - Read the X-Session-Id header
#   - Look up in Redis: GET session:<session_id>
#   - If found  → return {"user_id": "<user_id>"}
#   - If missing → return 401 Unauthorized
#
# ============================================================

@app.post("/login")
def login(body: LoginRequest):
    # TODO: implement session creation
    raise HTTPException(status_code=501, detail="Not implemented")


@app.get("/me")
def me(x_session_id: str = Header()):
    # TODO: implement session lookup
    raise HTTPException(status_code=501, detail="Not implemented")


# ============================================================
# Task 2: Rate Limiter (Fixed Window)
# ============================================================
#
# GET /request?user_id=<id>
#   - Key pattern: requests:user:<user_id>
#   - Use counter variable which expires in 60 seconds 
#   - If count > 5  → return 429 with {"error": "rate limit exceeded"}
#   - Otherwise     → return 200 with {"status": "ok", "remaining": 5 - count}
# ============================================================

@app.get("/request")
def rate_limited_request(user_id: str):
    # TODO: implement rate limiting
    raise HTTPException(status_code=501, detail="Not implemented")


# ============================================================
# Task 3: Task Queue (FIFO)
# ============================================================
#
# POST /task
#   - Accept JSON body: {"task": "send_email"}
#   - Push to the LEFT of a Redis list called "task_queue":
#         LPUSH task_queue <task>
#   - Return: {"status": "queued", "queue_length": <length>}
#
# GET /task
#   - Pop from the RIGHT of the list 
#   - If a task was returned → {"task": "<task>"}
#   - If the queue is empty  → 404 with {"error": "queue is empty"}
# ============================================================

@app.post("/task")
def add_task(body: TaskRequest):
    # TODO: implement task enqueue
    raise HTTPException(status_code=501, detail="Not implemented")


@app.get("/task")
def get_task():
    # TODO: implement task dequeue
    raise HTTPException(status_code=501, detail="Not implemented")


# ============================================================
# BONUS: Sliding Window Rate Limiter 
# ============================================================

@app.get("/request_sliding")
def rate_limited_request_sliding(user_id: str):
    pass