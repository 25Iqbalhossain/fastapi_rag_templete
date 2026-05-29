import os
import tempfile
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

TEST_DIR = tempfile.mkdtemp(prefix="industry-ai-tests-")

os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DIR}/test.db"
os.environ["REDIS_URL"] = "memory://"
os.environ["CELERY_BROKER_URL"] = "redis://localhost:6379/14"
os.environ["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/13"
os.environ["API_PREFIX"] = "/api/v1"
os.environ["METRICS_PATH"] = "/metrics"
os.environ["VECTOR_DB"] = "memory"
os.environ["LLM_PROVIDER"] = "echo"
os.environ["QUEUE_PROVIDER"] = "memory"
os.environ["SECRET_KEY"] = "test-secret"

from app.main import app
from app.core.config import get_settings


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
            yield async_client


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient) -> dict[str, str]:
    settings = get_settings()
    await client.post(
        f"{settings.api_prefix}/auth/register",
        json={
            "email": "user@example.com",
            "full_name": "Test User",
            "password": "Password123",
        },
    )
    response = await client.post(
        f"{settings.api_prefix}/auth/login",
        json={"email": "user@example.com", "password": "Password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}