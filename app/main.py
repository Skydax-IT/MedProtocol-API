from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import install_error_handlers
from app.api.middleware import InMemoryRateLimitMiddleware, RequestContextMiddleware
from app.api.router import router
from app.config import get_settings
from app.logging import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(
        title="MedProtocol API",
        version=settings.version,
        description=(
            "Demo-only deterministic protocol triage API. "
            "Not clinically validated and not for real patient care."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.state.settings = settings

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(InMemoryRateLimitMiddleware, settings=settings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origin_list,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["X-API-Key", "X-Request-ID", "X-Correlation-ID", "Content-Type"],
    )
    install_error_handlers(app)
    app.include_router(router)
    return app


app = create_app()
