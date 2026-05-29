import pytest

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.asyncio
async def test_rag_query_returns_retrieved_context(client, auth_headers):
    ingest_response = await client.post(
        f"{settings.api_prefix}/rag/documents",
        headers=auth_headers,
        json={
            "document_id": "doc-1",
            "text": "FastAPI works well for async APIs. Qdrant stores vectors for semantic search.",
        },
    )
    assert ingest_response.status_code == 200
    assert ingest_response.json()["chunks_indexed"] >= 1

    query_response = await client.post(
        f"{settings.api_prefix}/rag/query",
        headers=auth_headers,
        json={"query": "Which system stores vectors?", "limit": 2, "include_debug": True},
    )
    assert query_response.status_code == 200
    body = query_response.json()
    assert body["matches"]
    assert "Qdrant stores vectors" in body["answer"]
    assert body["debug"]["retrieved_count"] >= body["debug"]["reranked_count"]


@pytest.mark.asyncio
async def test_rag_reingest_replaces_document_for_same_user(client, auth_headers):
    first = await client.post(
        f"{settings.api_prefix}/rag/documents",
        headers=auth_headers,
        json={"document_id": "doc-2", "text": "Old content about oranges."},
    )
    assert first.status_code == 200

    second = await client.post(
        f"{settings.api_prefix}/rag/documents",
        headers=auth_headers,
        json={"document_id": "doc-2", "text": "New content about apples."},
    )
    assert second.status_code == 200

    query_response = await client.post(
        f"{settings.api_prefix}/rag/query",
        headers=auth_headers,
        json={"query": "What is the latest content?", "limit": 3, "document_id": "doc-2"},
    )
    assert query_response.status_code == 200
    body = query_response.json()
    joined = " ".join(match["text"] for match in body["matches"])
    assert "New content about apples." in joined
    assert "Old content about oranges." not in joined


@pytest.mark.asyncio
async def test_rag_isolation_prevents_cross_user_retrieval(client, auth_headers):
    ingest_response = await client.post(
        f"{settings.api_prefix}/rag/documents",
        headers=auth_headers,
        json={"document_id": "private-doc", "text": "Private finance strategy for user one."},
    )
    assert ingest_response.status_code == 200

    await client.post(
        f"{settings.api_prefix}/auth/register",
        json={
            "email": "other@example.com",
            "full_name": "Other User",
            "password": "Password123",
        },
    )
    login = await client.post(
        f"{settings.api_prefix}/auth/login",
        json={"email": "other@example.com", "password": "Password123"},
    )
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    query_response = await client.post(
        f"{settings.api_prefix}/rag/query",
        headers=other_headers,
        json={"query": "finance strategy", "limit": 3},
    )
    assert query_response.status_code == 200
    body = query_response.json()
    joined = " ".join(match["text"] for match in body["matches"])
    assert "Private finance strategy for user one." not in joined


@pytest.mark.asyncio
async def test_background_ingestion_uses_user_aware_queue_contract(client, auth_headers):
    response = await client.post(
        f"{settings.api_prefix}/rag/documents?background=true",
        headers=auth_headers,
        json={"document_id": "queued-doc", "text": "Queued user-specific content."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["queued"] is True
    assert body["task_id"].startswith("in-memory-1-queued-doc-")