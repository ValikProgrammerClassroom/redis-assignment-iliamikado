import pytest
import redis


@pytest.fixture(autouse=True)
def flush_redis():
    """Clear Redis before and after each test to ensure isolation."""
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.flushdb()
    yield
    r.flushdb()
