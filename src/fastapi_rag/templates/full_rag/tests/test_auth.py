import pytest

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.asyncio
async def test_register_and_login(client):
    register_response = await client.post(
        f"{settings.api_prefix}/auth/register",
        json={
            "email": "auth@example.com",
            "full_name": "Auth User",
            "password": "Password123",
        },
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "auth@example.com"

    login_response = await client.post(
        f"{settings.api_prefix}/auth/login",
        json={"email": "auth@example.com", "password": "Password123"},
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


@pytest.mark.asyncio
async def test_protected_route_requires_bearer_token(client, auth_headers):
    response = await client.get(f"{settings.api_prefix}/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
