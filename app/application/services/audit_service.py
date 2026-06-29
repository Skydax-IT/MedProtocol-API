from __future__ import annotations

from sqlalchemy.orm import Session

from app.api.errors import not_found
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.infrastructure.repositories.audit_repository import AuditRepository
from app.schemas.audit import AuditEventResponse
from app.schemas.common import ResponseMeta


class AuditService:
    def __init__(self, session: Session, tenant: AuthenticatedTenant, request_id: str) -> None:
        self.session = session
        self.tenant = tenant
        self.request_id = request_id
        self.repository = AuditRepository()

    def get_audit_event(self, audit_id: str) -> AuditEventResponse:
        event = self.repository.get_for_tenant(self.session, audit_id, self.tenant.tenant_id)
        if event is None:
            raise not_found("AUDIT_NOT_FOUND", f"Audit event {audit_id} was not found.")
        return AuditEventResponse(
            audit_id=event.audit_id,
            request_id=event.request_id,
            tenant_id=event.tenant_id,
            api_key_id=event.api_key_id,
            external_encounter_id=event.external_encounter_id,
            country_code=event.country_code,
            module=event.module,
            user_role=event.user_role,
            input_summary=event.input_summary,
            normalized_input=event.normalized_input,
            triggered_rules=event.triggered_rules,
            missing_critical_data=event.missing_critical_data,
            output=event.output,
            protocol_metadata=event.protocol_metadata,
            clinical_use_status=event.clinical_use_status,
            created_at=event.created_at,
            meta=ResponseMeta(request_id=self.request_id, tenant_id=self.tenant.tenant_id),
        )
