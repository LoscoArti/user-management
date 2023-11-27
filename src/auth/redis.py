from redis.asyncio import ConnectionPool, Redis

from src.config import settings

redis_client = None


async def get_redis_client() -> Redis:
    global redis_client
    if redis_client is None:
        pool = ConnectionPool.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            encoding="utf-8",
        )
        redis_client = Redis(connection_pool=pool)
    return redis_client


async def close_redis_client():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def add_token_to_blacklist(
    token: str, expiry_time_in_seconds: int = 1800
) -> None:
    client = await get_redis_client()
    await client.setex(token, expiry_time_in_seconds, "blacklisted")


async def is_token_blacklisted(token: str) -> bool:
    client = await get_redis_client()
    return await client.exists(token) > 0
