
from fastapi import FastAPI
import redis
import os
import time
import uvicorn

app = FastAPI()

# Connect to Redis using the Docker Compose service name
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    db=0,
    decode_responses=True,
    socket_connect_timeout=2,
)

def get_hit_count():
    retries = 5

    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.RedisError:
            retries -= 1

            if retries == 0:
                raise

            time.sleep(0.5)


@app.get("/")
async def index():
    return {"message": "Hello Docker Compose"}


@app.get("/hits")
async def hit():
    count = get_hit_count()
    return {"message": f"I have been hit {count} times."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)