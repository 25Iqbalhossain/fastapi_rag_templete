from app.core.config import Settings
from app.providers.database.base import BaseDatabaseProvider
from app.providers.database.sqlalchemy import SQLAlchemyDatabaseProvider


def get_database_provider(settings: Settings) -> BaseDatabaseProvider:
    provider = settings.database_provider.lower()
    if provider in {"postgres", "postgresql"}:
        return SQLAlchemyDatabaseProvider(settings.database_url)
    if provider == "mysql":
        return SQLAlchemyDatabaseProvider(settings.mysql_url or settings.database_url)
    if provider == "mongodb":
        raise ValueError(
            "MongoDB is not yet a drop-in provider for this template because the auth and "
            "repository layer currently depends on SQLAlchemy sessions. Use PostgreSQL or "
            "MySQL until the persistence layer is fully generalized."
        )
    raise ValueError(f"Unsupported database provider: {settings.database_provider}")
