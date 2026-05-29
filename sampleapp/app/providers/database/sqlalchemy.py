from app.db.session import DatabaseSessionManager
from app.providers.database.base import BaseDatabaseProvider


class SQLAlchemyDatabaseProvider(BaseDatabaseProvider):
    def __init__(self, database_url: str) -> None:
        self._session_manager = DatabaseSessionManager(database_url)

    @property
    def session_manager(self) -> DatabaseSessionManager:
        return self._session_manager

    async def connect(self) -> None:
        await self._session_manager.healthcheck(strict=True)

    async def migrate(self) -> None:
        await self._session_manager.create_all()

    async def healthcheck(self) -> bool:
        return await self._session_manager.healthcheck()

    async def close(self) -> None:
        await self._session_manager.close()