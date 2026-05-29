from app.core.config import Settings
from app.providers.cache.base import BaseCacheProvider
from app.providers.cache.dragonfly import DragonflyCacheProvider
from app.providers.cache.memory import InMemoryCacheProvider
from app.providers.cache.redis import RedisCacheProvider


def get_cache_provider(settings: Settings) -> BaseCacheProvider:
    provider = settings.cache_provider.lower()
    if provider == "memory" or settings.redis_url.startswith("memory://"):
        return InMemoryCacheProvider()
    if provider == "redis":
        return RedisCacheProvider(settings.redis_url)
    if provider == "dragonfly":
        return DragonflyCacheProvider(settings.dragonfly_url or settings.redis_url)
    raise ValueError(f"Unsupported cache provider: {settings.cache_provider}")