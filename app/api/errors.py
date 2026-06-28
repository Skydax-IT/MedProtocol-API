from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.domain.exceptions import DomainError
from app.schemas.errors import ErrorBody, ErrorDetail, ErrorMeta, ErrorResponse, validation_details

logger = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: list[ErrorDetail] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def api_error_handler(request: Request, exc: ApiError) -> JSONResponse:
        return _error_response(
            request=request,
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _error_response(
            request=request,
            code="VALIDATION_ERROR",
            message="Invalid request payload.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=validation_details(exc.errors()),
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        if exc.code == "COUNTRY_NOT_ENABLED":
            status_code = status.HTTP_403_FORBIDDEN
        if exc.code == "MODULE_NOT_ENABLED":
            status_code = status.HTTP_403_FORBIDDEN
        return _error_response(
            request=request,
            code=exc.code,
            message=str(exc) or "Domain error.",
            status_code=status_code,
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled request error",
            extra={
                "request_id": getattr(request.state, "request_id", "req_unknown"),
                "path": request.url.path,
                "method": request.method,
            },
        )
        return _error_response(
            request=request,
            code="INTERNAL_ERROR",
            message="Internal server error.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _error_response(
    *,
    request: Request,
    code: str,
    message: str,
    status_code: int,
    details: list[ErrorDetail] | None = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "req_unknown")
    body = ErrorResponse(
        error=ErrorBody(code=code, message=message, details=details or []),
        meta=ErrorMeta(request_id=request_id),
    )
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


def not_found(code: str, message: str) -> ApiError:
    return ApiError(code=code, message=message, status_code=status.HTTP_404_NOT_FOUND)


def forbidden(code: str, message: str) -> ApiError:
    return ApiError(code=code, message=message, status_code=status.HTTP_403_FORBIDDEN)


def unauthorized(message: str = "Missing or invalid API key.") -> ApiError:
    return ApiError(
        code="UNAUTHORIZED",
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return value
