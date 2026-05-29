import pytest

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.asyncio
async def test_metrics_endpoint_exposes_prometheus_payload(client):
    response = await client.get(settings.metrics_path)
    assert response.status_code == 200
    assert "http_requests_total" in response.text
