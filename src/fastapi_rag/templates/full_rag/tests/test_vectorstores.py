from app.core.config import Settings
from app.providers.vectorstores.factory import get_vectorstore
from app.providers.vectorstores.memory import InMemoryVectorStore
from app.services.embeddings import EmbeddingService


def test_vectorstore_factory_selects_memory_provider() -> None:
    settings = Settings(VECTOR_DB="memory")
    provider = get_vectorstore(settings, EmbeddingService(settings.embedding_dimensions))
    assert isinstance(provider, InMemoryVectorStore)
