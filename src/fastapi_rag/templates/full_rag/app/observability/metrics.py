import time

from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import get_settings


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

settings = get_settings()
router = APIRouter(tags=["metrics"])


@router.get(settings.metrics_path, include_in_schema=False)
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        latency = time.perf_counter() - start
        path = request.url.path
        REQUEST_COUNT.labels(request.method, path, str(response.status_code)).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(latency)
        return response
