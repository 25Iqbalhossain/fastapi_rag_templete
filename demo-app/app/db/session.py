from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.models.user import User  # noqa: F401


class DatabaseSessionManager:
    def __init__(self, database_url: str) -> None:
        self.engine = create_async_engine(database_url, future=True, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def healthcheck(self, strict: bool = False) -> bool:
        try:
            async with self.engine.begin() as connection:
                await connection.exec_driver_sql("SELECT 1")
                return True
        except Exception:
            return False

    async def close(self) -> None:
        await self.engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session