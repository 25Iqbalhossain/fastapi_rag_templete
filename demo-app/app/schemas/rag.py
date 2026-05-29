from pydantic import BaseModel, Field


class IngestDocumentRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1)


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=3, ge=1, le=10)
    document_id: str | None = Field(default=None, min_length=1, max_length=128)
    include_debug: bool = False


class RetrievedChunk(BaseModel):
    chunk_id: str
    score: float
    text: str


class QueryResponse(BaseModel):
    answer: str
    matches: list[RetrievedChunk]
    debug: dict[str, object] | None = None