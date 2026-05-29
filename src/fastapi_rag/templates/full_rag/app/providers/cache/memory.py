from app.providers.cache.base import BaseCacheProvider


class InMemoryCacheProvider(BaseCacheProvider):
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def connect(self) -> None:
        return None

    async def close(self) -> None:
        self.store.clear()

    async def healthcheck(self) -> bool:
        return True

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        self.store[key] = value

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)
