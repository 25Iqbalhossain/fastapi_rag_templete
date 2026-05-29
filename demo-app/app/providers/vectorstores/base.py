from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class VectorDocument:
    id: str
    text: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class VectorSearchResult:
    id: str
    score: float
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseVectorStore(ABC):
    @abstractmethod
    async def create_collection(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_documents(self, documents: list[VectorDocument]) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def similarity_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        raise NotImplementedError

    @abstractmethod
    async def delete_documents(self, document_ids: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_filters(self, filters: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def healthcheck(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError