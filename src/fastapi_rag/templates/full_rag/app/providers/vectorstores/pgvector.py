from typing import Any

from sqlalchemy import bindparam, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import Settings
from app.providers.vectorstores.base import BaseVectorStore, VectorDocument, VectorSearchResult
from app.services.embeddings import EmbeddingService


class PGVectorProvider(BaseVectorStore):
    def __init__(self, settings: Settings, embeddings: EmbeddingService) -> None:
        self.settings = settings
        self.embeddings = embeddings
        self.table_name = settings.pgvector_table_name
        self.engine: AsyncEngine = create_async_engine(
            settings.pgvector_url or settings.database_url,
            future=True,
            pool_pre_ping=True,
        )

    async def create_collection(self) -> None:
        async with self.engine.begin() as connection:
            await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            await connection.execute(
                text(
                    f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id TEXT PRIMARY KEY,
                        content TEXT NOT NULL,
                        metadata JSONB NOT NULL DEFAULT '{}',
                        embedding vector({self.settings.embedding_dimensions}) NOT NULL
                    )
                    """
                )
            )

    async def insert_documents(self, documents: list[VectorDocument]) -> list[str]:
        await self.create_collection()
        if not documents:
            return []
        async with self.engine.begin() as connection:
            for document in documents:
                await connection.execute(
                    text(
                        f"""
                        INSERT INTO {self.table_name} (id, content, metadata, embedding)
                        VALUES (:id, :content, CAST(:metadata AS JSONB), :embedding)
                        ON CONFLICT (id)
                        DO UPDATE SET
                            content = EXCLUDED.content,
                            metadata = EXCLUDED.metadata,
                            embedding = EXCLUDED.embedding
                        """
                    ),
                    {
                        "id": document.id,
                        "content": document.text,
                        "metadata": self._to_json(document.metadata),
                        "embedding": self._vector_literal(document.embedding),
                    },
                )
        return [document.id for document in documents]

    async def similarity_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        await self.create_collection()
        query_embedding = await self.embeddings.embed_text(query)
        sql = f"""
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> :embedding) AS score
            FROM {self.table_name}
        """
        params: dict[str, Any] = {"embedding": self._vector_literal(query_embedding), "limit": limit}
        if filters:
            predicates = []
            for index, (key, value) in enumerate(filters.items()):
                param_name = f"filter_{index}"
                predicates.append(f"metadata ->> '{key}' = :{param_name}")
                params[param_name] = str(value)
            sql += " WHERE " + " AND ".join(predicates)
        sql += " ORDER BY embedding <=> :embedding LIMIT :limit"
        async with self.engine.begin() as connection:
            result = await connection.execute(text(sql), params)
            rows = result.mappings().all()
        return [
            VectorSearchResult(
                id=str(row["id"]),
                score=float(row["score"]),
                text=str(row["content"]),
                metadata=dict(row["metadata"] or {}),
            )
            for row in rows
        ]

    async def delete_documents(self, document_ids: list[str]) -> None:
        if not document_ids:
            return
        statement = text(f"DELETE FROM {self.table_name} WHERE id IN :document_ids").bindparams(
            bindparam("document_ids", expanding=True)
        )
        async with self.engine.begin() as connection:
            await connection.execute(statement, {"document_ids": document_ids})

    async def delete_by_filters(self, filters: dict[str, Any]) -> None:
        if not filters:
            return
        predicates = []
        params: dict[str, Any] = {}
        for index, (key, value) in enumerate(filters.items()):
            param_name = f"filter_{index}"
            predicates.append(f"metadata ->> '{key}' = :{param_name}")
            params[param_name] = str(value)
        statement = text(f"DELETE FROM {self.table_name} WHERE " + " AND ".join(predicates))
        async with self.engine.begin() as connection:
            await connection.execute(statement, params)

    async def healthcheck(self) -> bool:
        try:
            async with self.engine.begin() as connection:
                await connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    async def close(self) -> None:
        await self.engine.dispose()

    def _vector_literal(self, values: list[float]) -> str:
        return "[" + ",".join(f"{value:.12f}" for value in values) + "]"

    def _to_json(self, payload: dict[str, Any]) -> str:
        import json

        return json.dumps(payload)
