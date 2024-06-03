from fastapi import FastAPI
import aioredis

app = FastAPI()

async def get_redis_connection():
    return await aioredis.create_redis_pool("redis://redis")

@app.get("/")
async def read_root():
    redis = await get_redis_connection()
    await redis.set("key", "value")
    value = await redis.get("key")
    return {"message": value}
