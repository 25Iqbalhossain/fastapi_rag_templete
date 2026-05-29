from math import sqrt
from uuid import uuid4

from typing import Any

from app.providers.vectorstores.base import BaseVectorStore, VectorDocument, VectorSearchResult
from app.services.embeddings import EmbeddingService


class InMemoryVectorStore(BaseVectorStore):
    def __init__(self, embeddings: EmbeddingService) -> None:
        self.embeddings = embeddings
        self.records: list[tuple[str, list[float], str, dict[str, Any]]] = []

    async def create_collection(self) -> None:
        return None

    async def insert_documents(self, documents: list[VectorDocument]) -> list[str]:
        inserted_ids: list[str] = []
        for document in documents:
            record_id = document.id or uuid4().hex
            self.records.append((record_id, document.embedding, document.text, document.metadata))
            inserted_ids.append(record_id)
        return inserted_ids

    async def similarity_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        query_vector = await self.embeddings.embed_text(query)
        scored = []
        for record_id, vector, text, metadata in self.records:
            if filters and any(str(metadata.get(key)) != str(value) for key, value in filters.items()):
                continue
            score = self._cosine_similarity(query_vector, vector)
            scored.append(
                VectorSearchResult(
                    id=record_id,
                    score=score,
                    text=text,
                    metadata=metadata,
                )
            )
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:limit]

    async def delete_documents(self, document_ids: list[str]) -> None:
        document_id_set = set(document_ids)
        self.records = [record for record in self.records if record[0] not in document_id_set]

    async def delete_by_filters(self, filters: dict[str, Any]) -> None:
        self.records = [
            record
            for record in self.records
            if any(str(record[3].get(key)) != str(value) for key, value in filters.items())
        ]

    async def healthcheck(self) -> bool:
        return True

    async def close(self) -> None:
        self.records.clear()

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        numerator = sum(a * b for a, b in zip(left, right, strict=False))
        left_norm = sqrt(sum(value * value for value in left)) or 1.0
        right_norm = sqrt(sum(value * value for value in right)) or 1.0
        return numerator / (left_norm * right_norm)