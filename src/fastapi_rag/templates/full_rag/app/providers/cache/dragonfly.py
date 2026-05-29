from app.providers.cache.redis import RedisCacheProvider


class DragonflyCacheProvider(RedisCacheProvider):
    """Dragonfly exposes the Redis protocol, so the Redis client is reusable."""
