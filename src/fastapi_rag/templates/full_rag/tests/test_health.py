import pytest


@pytest.mark.asyncio
async def test_health_endpoints(client):
    health = await client.get("/health")
    live = await client.get("/live")
    ready = await client.get("/ready")

    assert health.status_code == 200
    assert live.status_code == 200
    assert ready.status_code == 200
    assert health.json()["status"] == "healthy"
    assert live.json()["status"] == "alive"
    assert ready.json()["status"] == "ready"
