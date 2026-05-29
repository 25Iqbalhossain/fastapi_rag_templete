from uuid import uuid4

from app.providers.queues.base import BaseQueueProvider


class InMemoryQueueProvider(BaseQueueProvider):
    async def healthcheck(self) -> bool:
        return True

    async def close(self) -> None:
        return None

    def enqueue_document_ingestion(self, user_id: int, document_id: str, text: str) -> str:
        return f"in-memory-{user_id}-{document_id}-{uuid4().hex[:8]}"
