from __future__ import annotations

import time
import uuid
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import Settings


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or "req_" + uuid.uuid4().hex
        correlation_id = request.headers.get("X-Correlation-ID") or request_id
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    """Small MVP limiter for accidental abuse. Use an API gateway/Redis in production."""

    def __init__(self, app: object, settings: Settings) -> None:
        super().__init__(app)
        self.limit = settings.rate_limit_per_minute
        self.window_seconds = 60
        self._hits: defaultdict[str, deque[float]] = defaultdict(deque)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if self.limit <= 0:
            return await call_next(request)

        raw_key = request.headers.get("X-API-Key")
        identity = (
            raw_key[:16] if raw_key else (request.client.host if request.client else "unknown")
        )
        now = time.monotonic()
        bucket = self._hits[identity]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            return Response(
                content='{"error":{"code":"RATE_LIMITED","message":"Too many requests."}}',
                media_type="application/json",
                status_code=429,
            )
        bucket.append(now)
        return await call_next(request)
