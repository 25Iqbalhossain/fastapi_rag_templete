from app.providers.cache.base import BaseCacheProvider


class CacheService:
    def __init__(self, provider: BaseCacheProvider) -> None:
        self.provider = provider

    async def connect(self) -> None:
        await self.provider.connect()

    async def close(self) -> None:
        await self.provider.close()

    async def healthcheck(self) -> bool:
        return await self.provider.healthcheck()

    async def get(self, key: str) -> str | None:
        return await self.provider.get(key)

    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        await self.provider.set(key, value, ttl_seconds)

    async def delete(self, key: str) -> None:
        await self.provider.delete(key)

    async def cache_json(self, key: str, value: str, ttl_seconds: int = 300) -> None:
        await self.provider.set(key, value, ttl_seconds)