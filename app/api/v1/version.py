from __future__ import annotations

from fastapi import APIRouter

from app.config import get_settings
from app.schemas.common import VersionResponse

router = APIRouter(tags=["system"])


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(
        service=settings.service_name,
        version=settings.version,
        commit=settings.commit,
        environment=settings.environment,
    )
