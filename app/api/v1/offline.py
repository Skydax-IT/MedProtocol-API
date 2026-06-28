from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_authenticated_tenant
from app.application.services.offline_bundle_service import OfflineBundleService
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.schemas.offline import OfflineBundleResponse

router = APIRouter(prefix="/offline", tags=["offline"])


@router.get("/bundles/{country_code}/{module_code}", response_model=OfflineBundleResponse)
def get_offline_bundle(
    country_code: str,
    module_code: str,
    request: Request,
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
) -> OfflineBundleResponse:
    return OfflineBundleService(
        tenant=tenant,
        request_id=request.state.request_id,
    ).get_bundle(country_code=country_code, module_code=module_code)
