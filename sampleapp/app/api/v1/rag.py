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


@router.post("/upload", response_model=DocumentRead)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    doc_repo: DocumentRepository = Depends(get_document_repository),
) -> DocumentRead:
    # Ensure storage directory exists
    storage_dir = Path("storage/documents")
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_id = str(uuid.uuid4())
    file_path = storage_dir / f"{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Create DB record
    doc = await doc_repo.create(
        user_id=current_user.id,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        storage_path=str(file_path),
    )
    
    # Trigger background task
    process_document_task.delay(doc.id)
    
    return DocumentRead.model_validate(doc)


@router.get("/documents", response_model=list[DocumentRead])
async def list_documents(
    current_user: User = Depends(get_current_user),
    doc_repo: DocumentRepository = Depends(get_document_repository),
) -> list[DocumentRead]:
    docs = await doc_repo.list_by_user(current_user.id)
    return [DocumentRead.model_validate(doc) for doc in docs]


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