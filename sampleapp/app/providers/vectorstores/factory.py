from app.core.config import Settings
from app.providers.vectorstores.base import BaseVectorStore
from app.providers.vectorstores.memory import InMemoryVectorStore
from app.services.embeddings import EmbeddingService


def get_vectorstore(
    settings: Settings,
    embeddings: EmbeddingService,
) -> BaseVectorStore:
    provider = settings.vectorstore_provider.lower()
    if provider == "qdrant":
        from app.providers.vectorstores.qdrant import QdrantProvider

        return QdrantProvider(settings, embeddings)
    if provider == "chroma":
        from app.providers.vectorstores.chroma import ChromaProvider

        return ChromaProvider(settings, embeddings)
    if provider == "pgvector":
        from app.providers.vectorstores.pgvector import PGVectorProvider

        return PGVectorProvider(settings, embeddings)
    if provider == "pinecone":
        from app.providers.vectorstores.pinecone import PineconeProvider

        return PineconeProvider(settings, embeddings)
    if provider == "memory":
        return InMemoryVectorStore(embeddings)
    raise ValueError(f"Unsupported vector database provider: {settings.vectorstore_provider}")