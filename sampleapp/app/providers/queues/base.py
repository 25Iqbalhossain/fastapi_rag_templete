from abc import ABC, abstractmethod


class BaseQueueProvider(ABC):
    @abstractmethod
    async def healthcheck(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def enqueue_document_ingestion(self, user_id: int, document_id: str, text: str) -> str:
        raise NotImplementedError