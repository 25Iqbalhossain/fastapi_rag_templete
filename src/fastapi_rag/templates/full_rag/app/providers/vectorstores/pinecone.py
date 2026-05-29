from typing import Any

import anyio
from pinecone import Pinecone, ServerlessSpec

from app.core.config import Settings
from app.providers.vectorstores.base import BaseVectorStore, VectorDocument, VectorSearchResult
from app.services.embeddings import EmbeddingService


class PineconeProvider(BaseVectorStore):
    def __init__(self, settings: Settings, embeddings: EmbeddingService) -> None:
        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is required for pinecone provider")
        self.settings = settings
        self.embeddings = embeddings
        self.client = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name

    async def create_collection(self) -> None:
        index_names = await anyio.to_thread.run_sync(
            lambda: list(self.client.list_indexes().names())
        )
        if self.index_name in index_names:
            return
        await anyio.to_thread.run_sync(
            lambda: self.client.create_index(
                name=self.index_name,
                dimension=self.settings.embedding_dimensions,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=self.settings.pinecone_cloud,
                    region=self.settings.pinecone_region,
                ),
            )
        )

    async def insert_documents(self, documents: list[VectorDocument]) -> list[str]:
        await self.create_collection()
        if not documents:
            return []
        index = self.client.Index(self.index_name)
        vectors = [
            {
                "id": document.id,
                "values": document.embedding,
                "metadata": {"text": document.text, **document.metadata},
            }
            for document in documents
        ]
        await anyio.to_thread.run_sync(lambda: index.upsert(vectors=vectors))
        return [document.id for document in documents]

    async def similarity_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        await self.create_collection()
        query_embedding = await self.embeddings.embed_text(query)
        index = self.client.Index(self.index_name)
        response = await anyio.to_thread.run_sync(
            lambda: index.query(
                vector=query_embedding,
                top_k=limit,
                filter=filters,
                include_metadata=True,
            )
        )
        return [
            VectorSearchResult(
                id=str(match["id"]),
                score=float(match["score"]),
                text=str(match.get("metadata", {}).get("text", "")),
                metadata=dict(match.get("metadata", {})),
            )
            for match in response["matches"]
        ]

    async def delete_documents(self, document_ids: list[str]) -> None:
        if not document_ids:
            return
        index = self.client.Index(self.index_name)
        await anyio.to_thread.run_sync(lambda: index.delete(ids=document_ids))

    async def delete_by_filters(self, filters: dict[str, Any]) -> None:
        if not filters:
            return
        index = self.client.Index(self.index_name)
        await anyio.to_thread.run_sync(lambda: index.delete(filter=filters))

    async def healthcheck(self) -> bool:
        try:
            await anyio.to_thread.run_sync(lambda: list(self.client.list_indexes().names()))
            return True
        except Exception:
            return False

    async def close(self) -> None:
        return None
