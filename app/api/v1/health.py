from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.infrastructure.database import SessionLocal
from app.infrastructure.rules.loader import load_demo_catalog
from app.schemas.common import HealthResponse, ReadinessResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.service_name,
        timestamp=datetime.now(UTC).isoformat(),
    )


@router.get("/ready", response_model=ReadinessResponse)
def ready(response: Response) -> ReadinessResponse:
    settings = get_settings()
    checks = {
        "api": "ok",
        "database": "ok",
        "demo_rules": "ok",
    }

    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        checks["database"] = "error"

    try:
        catalog = load_demo_catalog()
        if not catalog.protocols or not catalog.rules or not catalog.country_packs:
            checks["demo_rules"] = "error"
    except (OSError, ValueError, KeyError):
        checks["demo_rules"] = "error"

    ready_status = "ready" if all(value == "ok" for value in checks.values()) else "not_ready"
    if ready_status != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        status=ready_status,
        service=settings.service_name,
        environment=settings.environment,
        checks=checks,
    )
