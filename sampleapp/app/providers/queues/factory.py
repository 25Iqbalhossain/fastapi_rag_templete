from app.core.config import Settings
from app.providers.queues.base import BaseQueueProvider
from app.providers.queues.celery import CeleryQueueProvider
from app.providers.queues.memory import InMemoryQueueProvider


def get_queue_provider(settings: Settings) -> BaseQueueProvider:
    provider = settings.queue_provider.lower()
    if provider == "memory":
        return InMemoryQueueProvider()
    if provider == "celery":
        return CeleryQueueProvider(settings)
    raise ValueError(f"Unsupported queue provider: {settings.queue_provider}")