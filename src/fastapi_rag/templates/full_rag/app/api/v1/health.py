from fastapi import APIRouter, Depends

from app.core.dependencies import ServiceContainer, get_container


router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/live")
async def live() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/ready")
async def ready(container: ServiceContainer = Depends(get_container)) -> dict[str, object]:
    checks = {}
    if container.db_provider is not None:
        checks["database"] = await container.db_provider.healthcheck()
    else:
        checks["database"] = False
    if container.cache is not None:
        checks["cache"] = await container.cache.healthcheck()
    else:
        checks["cache"] = False
    if container.vectorstore is not None:
        checks["vectorstore"] = await container.vectorstore.healthcheck()
    else:
        checks["vectorstore"] = False
    if container.queue is not None:
        checks["queue"] = await container.queue.healthcheck()
    else:
        checks["queue"] = False
    checks["llm"] = container.llm is not None
    ready_state = all(checks.values())
    return {
        "status": "ready" if ready_state else "not_ready",
        "checks": checks,
        "startup": {
            name: {"ready": state.ready, "error": state.error}
            for name, state in container.component_states.items()
        },
    }
