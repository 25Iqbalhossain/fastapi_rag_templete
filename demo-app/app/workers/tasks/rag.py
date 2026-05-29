from pathlib import Path
import asyncio

from app.core.config import get_settings
from app.core.dependencies import build_service_container
from app.db.models.document import DocumentStatus
from app.db.repositories.document_repository import DocumentRepository
from app.services.parsing import parse_file
from app.workers.celery_app import celery_app


async def _process_document(doc_id: int):
    settings = get_settings()
    container = await build_service_container(settings)
    
    async with container.db.session() as session:
        doc_repo = DocumentRepository(session)
        doc = await doc_repo.get_by_id(doc_id)
        if not doc:
            return

        await doc_repo.update_status(doc_id, DocumentStatus.PROCESSING)
        
        try:
            # Parse
            text = parse_file(Path(doc.storage_path), doc.content_type)
            
            # Ingest into RAG pipeline
            if container.rag_pipeline:
                await container.rag_pipeline.ingest_document(
                    user_id=doc.user_id,
                    document_id=str(doc.id),
                    text=text
                )
            
            await doc_repo.update_status(doc_id, DocumentStatus.COMPLETED)
        except Exception as exc:
            await doc_repo.update_status(doc_id, DocumentStatus.FAILED, error_message=str(exc))
        finally:
            await container.close()


@celery_app.task(name="app.workers.tasks.rag.process_document_task")
def process_document_task(doc_id: int):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(_process_document(doc_id))
    else:
        loop.run_until_complete(_process_document(doc_id))