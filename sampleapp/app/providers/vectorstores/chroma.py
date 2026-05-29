from typing import Any

import anyio
import chromadb

from app.core.config import Settings
from app.providers.vectorstores.base import BaseVectorStore, VectorDocument, VectorSearchResult
from app.services.embeddings import EmbeddingService


class ChromaProvider(BaseVectorStore):
    def __init__(self, settings: Settings, embeddings: EmbeddingService) -> None:
        self.settings = settings
        self.embeddings = embeddings
        self.collection_name = settings.chroma_collection_name
        self.client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
        )

    async def create_collection(self) -> None:
        await anyio.to_thread.run_sync(self.client.get_or_create_collection, self.collection_name)

    async def insert_documents(self, documents: list[VectorDocument]) -> list[str]:
        await self.create_collection()
        if not documents:
            return []
        collection = await self._get_collection()
        await anyio.to_thread.run_sync(
            lambda: collection.upsert(
                ids=[document.id for document in documents],
                documents=[document.text for document in documents],
                embeddings=[document.embedding for document in documents],
                metadatas=[document.metadata for document in documents],
            )
        )
        return [document.id for document in documents]

    async def similarity_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        await self.create_collection()
        collection = await self._get_collection()
        query_embedding = await self.embeddings.embed_text(query)
        response = await anyio.to_thread.run_sync(
            lambda: collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=filters,
            )
        )
        ids = response.get("ids", [[]])[0]
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]
        return [
            VectorSearchResult(
                id=str(record_id),
                score=float(1 - distance),
                text=str(text),
                metadata=dict(metadata or {}),
            )
            for record_id, text, metadata, distance in zip(
                ids,
                documents,
                metadatas,
                distances,
                strict=False,
            )
        ]

    async def delete_documents(self, document_ids: list[str]) -> None:
        if not document_ids:
            return
        collection = await self._get_collection()
        await anyio.to_thread.run_sync(lambda: collection.delete(ids=document_ids))

    async def delete_by_filters(self, filters: dict[str, Any]) -> None:
        if not filters:
            return
        collection = await self._get_collection()
        await anyio.to_thread.run_sync(lambda: collection.delete(where=filters))

    async def healthcheck(self) -> bool:
        try:
            await anyio.to_thread.run_sync(self.client.heartbeat)
            return True
        except Exception:
            return False

    async def close(self) -> None:
        return None

    async def _get_collection(self) -> Any:
        return await anyio.to_thread.run_sync(self.client.get_or_create_collection, self.collection_name)