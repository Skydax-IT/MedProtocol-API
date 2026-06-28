from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_authenticated_tenant
from app.application.services.protocol_service import ProtocolService
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.schemas.protocols import ProtocolDetailResponse, ProtocolListResponse

router = APIRouter(prefix="/protocols", tags=["protocols"])


@router.get("", response_model=ProtocolListResponse)
def list_protocols(
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
) -> ProtocolListResponse:
    del tenant
    return ProtocolListResponse(items=ProtocolService().list_protocols())


@router.get("/{protocol_id}", response_model=ProtocolDetailResponse)
def get_protocol(
    protocol_id: str,
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
) -> ProtocolDetailResponse:
    del tenant
    return ProtocolDetailResponse.model_validate(ProtocolService().get_protocol(protocol_id))
