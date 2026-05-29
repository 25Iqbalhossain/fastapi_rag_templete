from abc import ABC, abstractmethod

from app.db.session import DatabaseSessionManager


class BaseDatabaseProvider(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def migrate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def healthcheck(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def session_manager(self) -> DatabaseSessionManager | None:
        raise NotImplementedError