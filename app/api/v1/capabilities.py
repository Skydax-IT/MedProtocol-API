from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_authenticated_tenant
from app.application.services.capability_service import CapabilityService
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.schemas.capabilities import CapabilitiesResponse
from app.schemas.common import ResponseMeta

router = APIRouter(tags=["capabilities"])


@router.get("/capabilities", response_model=CapabilitiesResponse)
def capabilities(
    request: Request,
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
) -> CapabilitiesResponse:
    payload = CapabilityService().get_capabilities()
    payload["meta"] = ResponseMeta(
        request_id=request.state.request_id,
        tenant_id=tenant.tenant_id,
    ).model_dump(mode="json")
    return CapabilitiesResponse.model_validate(payload)
