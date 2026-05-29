from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.rag import router as rag_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.core.middleware import JwtValidationMiddleware, RequestContextMiddleware
from app.core.dependencies import ServiceContainer, build_service_container
from app.observability.metrics import MetricsMiddleware, router as metrics_router
from app.observability.tracing import configure_tracing


settings = get_settings()
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = await build_service_container(settings)
    app.state.container = container
    configure_tracing(app, settings, container.db_provider)
    logger.info("application_started", extra={"component": "startup"})
    try:
        yield
    finally:
        await container.close()
        logger.info("application_stopped", extra={"component": "shutdown"})


app = FastAPI(title=settings.project_name, lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(JwtValidationMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(rag_router)
app.include_router(metrics_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"{settings.project_name} running"}
