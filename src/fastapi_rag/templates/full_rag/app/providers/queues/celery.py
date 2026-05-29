from celery import Celery

from app.core.config import Settings
from app.providers.queues.base import BaseQueueProvider


class CeleryQueueProvider(BaseQueueProvider):
    def __init__(self, settings: Settings) -> None:
        self.app = Celery(
            "industry_ai_worker",
            broker=settings.celery_broker_url,
            backend=settings.celery_result_backend,
        )

    async def healthcheck(self) -> bool:
        try:
            with self.app.connection_for_read() as connection:
                connection.ensure_connection(max_retries=1)
            return True
        except Exception:
            return False

    async def close(self) -> None:
        return None

    def enqueue_document_ingestion(self, user_id: int, document_id: str, text: str) -> str:
        task = self.app.send_task(
            "app.tasks.ingest_document",
            args=[user_id, document_id, text],
        )
        return task.id
