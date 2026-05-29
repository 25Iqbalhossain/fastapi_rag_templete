from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.context import request_id_var
from app.core.logging import get_logger


logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_exception", extra={"component": "exception"})
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id_var.get(),
                "error": exc.__class__.__name__,
            },
        )