from redis.asyncio import Redis

from app.providers.cache.base import BaseCacheProvider


class RedisCacheProvider(BaseCacheProvider):
    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url
        self.client: Redis | None = None

    async def connect(self) -> None:
        self.client = Redis.from_url(self.redis_url, decode_responses=True)
        await self.client.ping()

    async def close(self) -> None:
        if self.client is not None:
            await self.client.aclose()

    async def healthcheck(self) -> bool:
        if self.client is None:
            return False
        try:
            await self.client.ping()
            return True
        except Exception:
            return False

    async def get(self, key: str) -> str | None:
        if self.client is None:
            return None
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        if self.client is not None:
            await self.client.set(key, value, ex=ttl_seconds)

    async def delete(self, key: str) -> None:
        if self.client is not None:
            await self.client.delete(key)
