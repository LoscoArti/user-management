from contextlib import asynccontextmanager

from redis.asyncio import ConnectionPool, Redis

from src.config import settings


@asynccontextmanager
async def get_redis_client() -> Redis:
    pool = ConnectionPool.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        encoding="utf-8",
    )
    client = Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.close()
        await pool.disconnect()


async def add_token_to_blacklist(
    token: str, expiry_time_in_seconds: int = 1800
) -> None:
    async with get_redis_client() as client:
        await client.setex(name=token, value="blacklisted", time=expiry_time_in_seconds)


async def is_token_blacklisted(token: str) -> bool:
    async with get_redis_client() as client:
        return await client.exists(token) > 0
