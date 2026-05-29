from dataclasses import dataclass, field

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.core.security import decode_access_token
from app.db.models.user import User
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.user_repository import UserRepository
from app.db.session import DatabaseSessionManager
from app.modules.agents.agent_manager import AgentManager
from app.modules.agents.implementations.rag_agent import RAGAgent
from app.modules.agents.implementations.sql_agent import SQLAgent
from app.modules.agents.implementations.weather_agent import WeatherAgent
from app.modules.agents.orchestrator import Orchestrator
from app.modules.rag.pipeline import RAGPipeline
from app.providers.cache import get_cache_provider
from app.providers.database import BaseDatabaseProvider, get_database_provider
from app.providers.llm import get_llm_provider
from app.providers.llm.base import BaseLLMProvider
from app.providers.queues import BaseQueueProvider, get_queue_provider
from app.providers.vectorstores import get_vectorstore
from app.providers.vectorstores.base import BaseVectorStore
from app.services.auth import AuthService
from app.services.embeddings import EmbeddingService
from app.services.redis import CacheService


settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")
logger = get_logger(__name__)


@dataclass
class DependencyState:
    ready: bool
    error: str | None = None


@dataclass
class ServiceContainer:
    settings: Settings
    embeddings: EmbeddingService
    db_provider: BaseDatabaseProvider | None = None
    db: DatabaseSessionManager | None = None
    cache: CacheService | None = None
    vectorstore: BaseVectorStore | None = None
    llm: BaseLLMProvider | None = None
    queue: BaseQueueProvider | None = None
    rag_pipeline: RAGPipeline | None = None
    agent_manager: AgentManager | None = None
    orchestrator: Orchestrator | None = None
    component_states: dict[str, DependencyState] = field(default_factory=dict)

    async def close(self) -> None:
        if self.cache is not None:
            await self.cache.close()
        if self.vectorstore is not None:
            await self.vectorstore.close()
        if self.queue is not None:
            await self.queue.close()
        if self.db_provider is not None:
            await self.db_provider.close()


async def build_service_container(settings: Settings) -> ServiceContainer:
    embeddings = EmbeddingService(settings.embedding_dimensions)
    component_states: dict[str, DependencyState] = {}

    db_provider: BaseDatabaseProvider | None = None
    db_session_manager: DatabaseSessionManager | None = None
    try:
        db_provider = get_database_provider(settings)
        await db_provider.connect()
        if settings.auto_migrate:
            await db_provider.migrate()
        db_session_manager = db_provider.session_manager
        component_states["database"] = DependencyState(ready=True)
    except Exception as exc:
        component_states["database"] = DependencyState(ready=False, error=str(exc))
        logger.exception("database_initialization_failed", extra={"component": "startup"})
        if not settings.startup_dependency_tolerance:
            raise

    cache: CacheService | None = None
    try:
        cache_provider = get_cache_provider(settings)
        cache = CacheService(cache_provider)
        await cache.connect()
        component_states["cache"] = DependencyState(ready=True)
    except Exception as exc:
        component_states["cache"] = DependencyState(ready=False, error=str(exc))
        logger.exception("cache_initialization_failed", extra={"component": "startup"})
        if not settings.startup_dependency_tolerance:
            raise

    vectorstore: BaseVectorStore | None = None
    try:
        vectorstore = get_vectorstore(settings, embeddings)
        await vectorstore.create_collection()
        component_states["vectorstore"] = DependencyState(ready=True)
    except Exception as exc:
        component_states["vectorstore"] = DependencyState(ready=False, error=str(exc))
        logger.exception("vectorstore_initialization_failed", extra={"component": "startup"})
        if not settings.startup_dependency_tolerance:
            raise

    llm: BaseLLMProvider | None = None
    try:
        llm = get_llm_provider(settings)
        component_states["llm"] = DependencyState(ready=True)
    except Exception as exc:
        component_states["llm"] = DependencyState(ready=False, error=str(exc))
        logger.exception("llm_initialization_failed", extra={"component": "startup"})
        if not settings.startup_dependency_tolerance:
            raise

    queue: BaseQueueProvider | None = None
    try:
        queue = get_queue_provider(settings)
        component_states["queue"] = DependencyState(ready=True)
    except Exception as exc:
        component_states["queue"] = DependencyState(ready=False, error=str(exc))
        logger.exception("queue_initialization_failed", extra={"component": "startup"})
        if not settings.startup_dependency_tolerance:
            raise

    rag_pipeline = None
    agent_manager = AgentManager()
    orchestrator = None
    
    if vectorstore is not None and llm is not None:
        rag_pipeline = RAGPipeline(
            embeddings=embeddings,
            vectorstore=vectorstore,
            llm=llm,
        )
        agent_manager.register(RAGAgent(rag_pipeline))
        orchestrator = Orchestrator(agent_manager, llm)

    if db_provider is not None:
        agent_manager.register(SQLAgent(db_provider))
    
    agent_manager.register(WeatherAgent())

    return ServiceContainer(
        settings=settings,
        db_provider=db_provider,
        db=db_session_manager,
        cache=cache,
        vectorstore=vectorstore,
        llm=llm,
        queue=queue,
        embeddings=embeddings,
        rag_pipeline=rag_pipeline,
        agent_manager=agent_manager,
        orchestrator=orchestrator,
        component_states=component_states,
    )


def get_container(request: Request) -> ServiceContainer:
    return request.app.state.container


def get_settings_dependency() -> Settings:
    return get_settings()


async def get_db_session(
    container: ServiceContainer = Depends(get_container),
) -> AsyncSession:
    if container.db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database dependency is unavailable",
        )
    async with container.db.session() as session:
        yield session


async def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings_dependency),
) -> AuthService:
    return AuthService(UserRepository(session), settings)


async def get_document_repository(
    session: AsyncSession = Depends(get_db_session),
) -> DocumentRepository:
    return DocumentRepository(session)


async def get_conversation_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ConversationRepository:
    return ConversationRepository(session)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings_dependency),
) -> User:
    payload = decode_access_token(token, settings)
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = await UserRepository(session).get_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def get_rag_pipeline(
    container: ServiceContainer = Depends(get_container),
) -> RAGPipeline:
    if container.rag_pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG dependencies are unavailable",
        )
    return container.rag_pipeline


async def get_agent_manager(
    container: ServiceContainer = Depends(get_container),
) -> AgentManager:
    if container.agent_manager is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent Manager is unavailable",
        )
    return container.agent_manager


async def get_orchestrator(
    container: ServiceContainer = Depends(get_container),
) -> Orchestrator:
    if container.orchestrator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator is unavailable",
        )
    return container.orchestrator