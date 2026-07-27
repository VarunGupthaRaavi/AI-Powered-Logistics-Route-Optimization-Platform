"""Global exception handlers and structured logging for FastAPI application."""

import logging
from typing import Any

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure structured application error logger
logger = logging.getLogger("routeai.errors")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions (400, 401, 403, 404, 409, 500) and format consistent JSON."""
    logger.warning("HTTP Exception %s on %s %s: %s", exc.status_code, request.method, request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle 422 Pydantic request validation errors and format structured field error details."""
    logger.warning("Validation Error 422 on %s %s: %s", request.method, request.url.path, exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Request validation failed",
            "errors": jsonable_encoder(exc.errors()),
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle database errors (SQLAlchemy IntegrityError/OperationalError).

    Logs full traceback internally for developer diagnostics, but returns a clean,
    sanitized error response to external users to avoid leaking internal DB schemas or credentials.
    """
    logger.error("Database Error on %s %s: %s", request.method, request.url.path, str(exc), exc_info=True)

    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Database conflict violation. A unique constraint or foreign key check failed."},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A database error occurred. Internal database state has been safely protected."},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all global exception handler for unexpected Python runtime crashes (500 Internal Server Error).

    Logs full stack trace internally and prevents raw stack traces from reaching production clients.
    """
    logger.critical("Unhandled Exception 500 on %s %s: %s", request.method, request.url.path, str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred. Please contact system support."},
    )
