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
        api_version=settings.version,
        demo_version=settings.demo_version,
        product_stage=settings.product_stage,
        clinical_status=settings.clinical_status,
        commit=settings.commit,
        environment=settings.environment,
    )
