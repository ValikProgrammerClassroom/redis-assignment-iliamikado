"""
Implement the TODO sections below using Redis commands.
Each endpoint corresponds to one graded task.

Run locally:
    uvicorn app:app --reload

Run tests:
    pytest tests/ -v
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis
import time
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
    session_id = str(uuid.uuid4())
    r.set(f"session:{session_id}", body.user_id, ex=3600)
    return {"session_id": session_id}


@app.get("/me")
def me(x_session_id: str = Header()):
    user_id = r.get(f"session:{x_session_id}")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": user_id}


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
    key = f"requests:user:{user_id}"
    pipe = r.pipeline(transaction=False)
    pipe.incr(key)
    pipe.expire(key, 60, nx=True)
    count, _ = pipe.execute()

    if count > 5:
        return JSONResponse(status_code=429, content={"error": "rate limit exceeded"})

    return {"status": "ok", "remaining": 5 - count}


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
    queue_length = r.lpush("task_queue", body.task)
    return {"status": "queued", "queue_length": queue_length}


@app.get("/task")
def get_task():
    task = r.rpop("task_queue")
    if task is None:
        return JSONResponse(status_code=404, content={"error": "queue is empty"})
    return {"task": task}


# ============================================================
# BONUS: Sliding Window Rate Limiter 
# ============================================================

@app.get("/request_sliding")
def rate_limited_request_sliding(user_id: str):
    key = f"requests:user:{user_id}"
    now = time.time()
    request_id = str(uuid.uuid4())

    pipe = r.pipeline(transaction=False)
    pipe.zremrangebyscore(key, 0, now - 60)
    pipe.zadd(key, {request_id: now})
    pipe.zcard(key)
    pipe.expire(key, 60)
    _, _, count, _ = pipe.execute()

    if count > 5:
        return JSONResponse(status_code=429, content={"error": "rate limit exceeded"})

    return {"status": "ok", "remaining": 5 - count}
