import asyncio

from app.core.config import get_settings
from app.core.dependencies import build_service_container
from app.providers.queues.celery import CeleryQueueProvider


settings = get_settings()
celery_app = CeleryQueueProvider(settings).app


@celery_app.task(name="app.tasks.ingest_document")
def ingest_document_task(user_id: int, document_id: str, text: str) -> dict[str, object]:
    return asyncio.run(_ingest_document(user_id, document_id, text))


async def _ingest_document(user_id: int, document_id: str, text: str) -> dict[str, object]:
    container = await build_service_container(settings)
    try:
        if container.rag_pipeline is None:
            raise RuntimeError("RAG pipeline unavailable")
        chunk_ids = await container.rag_pipeline.ingest_document(user_id, document_id, text)
        return {
            "user_id": user_id,
            "document_id": document_id,
            "chunk_ids": chunk_ids,
            "chunks_indexed": len(chunk_ids),
        }
    finally:
        await container.close()