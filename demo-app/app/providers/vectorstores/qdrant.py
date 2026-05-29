from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models

from app.core.config import Settings
from app.providers.vectorstores.base import BaseVectorStore, VectorDocument, VectorSearchResult
from app.services.embeddings import EmbeddingService


class QdrantProvider(BaseVectorStore):
    def __init__(self, settings: Settings, embeddings: EmbeddingService) -> None:
        self.settings = settings
        self.embeddings = embeddings
        self.collection_name = settings.qdrant_collection_name
        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    async def create_collection(self) -> None:
        exists = await self.client.collection_exists(self.collection_name)
        if exists:
            return
        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.settings.embedding_dimensions,
                distance=models.Distance.COSINE,
            ),
        )

    async def insert_documents(self, documents: list[VectorDocument]) -> list[str]:
        await self.create_collection()
        if not documents:
            return []
        points = [
            models.PointStruct(
                id=document.id,
                vector=document.embedding,
                payload={
                    "text": document.text,
                    **document.metadata,
                },
            )
            for document in documents
        ]
        await self.client.upsert(collection_name=self.collection_name, points=points)
        return [document.id for document in documents]

    async def similarity_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        await self.create_collection()
        query_embedding = await self.embeddings.embed_text(query)
        qdrant_filter = self._build_filter(filters)
        response = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
            query_filter=qdrant_filter,
            with_payload=True,
        )
        return [
            VectorSearchResult(
                id=str(point.id),
                score=float(point.score),
                text=str((point.payload or {}).get("text", "")),
                metadata=dict(point.payload or {}),
            )
            for point in response.points
        ]

    async def delete_documents(self, document_ids: list[str]) -> None:
        if not document_ids:
            return
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=document_ids),
        )

    async def delete_by_filters(self, filters: dict[str, Any]) -> None:
        qdrant_filter = self._build_filter(filters)
        if qdrant_filter is None:
            return
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(filter=qdrant_filter),
        )

    async def healthcheck(self) -> bool:
        try:
            await self.client.get_collections()
            return True
        except Exception:
            return False

    async def close(self) -> None:
        await self.client.close()

    def _build_filter(self, filters: dict[str, Any] | None) -> models.Filter | None:
        if not filters:
            return None
        conditions = [
            models.FieldCondition(
                key=key,
                match=models.MatchValue(value=value),
            )
            for key, value in filters.items()
        ]
        return models.Filter(must=conditions)