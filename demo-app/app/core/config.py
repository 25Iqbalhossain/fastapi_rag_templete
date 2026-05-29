from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    project_name: str = "demo-app"
    app_env: str = "development"
    debug: bool = False
    auto_migrate: bool = True
    startup_dependency_tolerance: bool = True

    api_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    trusted_hosts: list[str] = Field(default_factory=lambda: ["*"])
    metrics_path: str = "/metrics"

    secret_key: str = "iunYw68SjSdCHM6vdWQiJ0xDzyL0OKxnMO-1cUhMw1Q"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_provider: str = "postgresql"
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/industry_ai"
    mysql_url: str | None = None
    mongodb_url: str | None = None
    mongodb_database: str = "industry_ai"

    cache_provider: str = "redis"
    redis_url: str = "redis://redis:6379/0"
    dragonfly_url: str | None = None

    queue_provider: str = "celery"
    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"

    vectorstore_provider: str = Field(
        default="qdrant",
        validation_alias=AliasChoices("VECTOR_DB", "VECTORSTORE_PROVIDER"),
    )
    llm_provider: str = "echo"
    embedding_dimensions: int = 64

    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str | None = None
    qdrant_collection_name: str = "documents"
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_collection_name: str = "documents"
    pgvector_url: str | None = None
    pgvector_table_name: str = "document_embeddings"
    pinecone_api_key: str | None = None
    pinecone_index_name: str = "documents"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "llama3.1"

    otel_enabled: bool = False
    otel_service_name: str = "industry-ai-backend"
    otel_exporter_otlp_endpoint: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()