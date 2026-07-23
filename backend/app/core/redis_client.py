"""Redis connection helper (async)."""
import redis.asyncio as aioredis

from app.core.config import settings

redis_client: aioredis.Redis = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def ping_redis() -> bool:
    try:
        return await redis_client.ping()
    except Exception:
        return False
