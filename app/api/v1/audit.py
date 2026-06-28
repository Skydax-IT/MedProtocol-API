from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_authenticated_tenant, get_db
from app.application.services.audit_service import AuditService
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.schemas.audit import AuditEventResponse

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/{audit_id}", response_model=AuditEventResponse)
def get_audit_event(
    audit_id: str,
    request: Request,
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
    db: Annotated[Session, Depends(get_db)],
) -> AuditEventResponse:
    return AuditService(
        session=db,
        tenant=tenant,
        request_id=request.state.request_id,
    ).get_audit_event(audit_id)
