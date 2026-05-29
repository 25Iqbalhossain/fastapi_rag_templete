from fastapi import APIRouter, Depends, Query

from app.core.config import get_settings
from app.core.dependencies import ServiceContainer, get_container, get_current_user, get_rag_pipeline
from app.db.models.user import User
from app.modules.rag.pipeline import RAGPipeline
from app.schemas.rag import IngestDocumentRequest, QueryRequest, QueryResponse


settings = get_settings()
router = APIRouter(prefix=f"{settings.api_prefix}/rag", tags=["rag"])


@router.post("/documents")
async def ingest_document(
    payload: IngestDocumentRequest,
    background: bool = Query(default=False),
    current_user: User = Depends(get_current_user),
    container: ServiceContainer = Depends(get_container),
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> dict[str, object]:
    if background:
        if container.queue is None:
            return {"queued": False, "error": "Queue provider unavailable"}
        task_id = container.queue.enqueue_document_ingestion(
            current_user.id,
            payload.document_id,
            payload.text,
        )
        return {"queued": True, "task_id": task_id}
    chunk_ids = await rag_pipeline.ingest_document(current_user.id, payload.document_id, payload.text)
    return {"queued": False, "chunk_ids": chunk_ids, "chunks_indexed": len(chunk_ids)}


@router.post("/query", response_model=QueryResponse)
async def query_rag(
    payload: QueryRequest,
    current_user: User = Depends(get_current_user),
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> QueryResponse:
    return await rag_pipeline.run(
        user_id=current_user.id,
        query=payload.query,
        limit=payload.limit,
        document_id=payload.document_id,
        include_debug=payload.include_debug,
    )
