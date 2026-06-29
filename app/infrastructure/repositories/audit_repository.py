from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models import AuditEventModel


def new_audit_id() -> str:
    return "aud_" + uuid.uuid4().hex


class AuditRepository:
    def create(
        self,
        session: Session,
        *,
        tenant_id: str,
        api_key_id: str,
        request_id: str,
        external_encounter_id: str | None,
        country_code: str,
        module: str,
        user_role: str,
        input_summary: dict[str, Any],
        normalized_input: dict[str, Any],
        triggered_rules: list[str],
        missing_critical_data: list[str],
        output: dict[str, Any],
        protocol_metadata: dict[str, Any],
        clinical_use_status: str,
    ) -> AuditEventModel:
        event = AuditEventModel(
            audit_id=new_audit_id(),
            tenant_id=tenant_id,
            api_key_id=api_key_id,
            request_id=request_id,
            external_encounter_id=external_encounter_id,
            country_code=country_code,
            module=module,
            user_role=user_role,
            input_summary=input_summary,
            normalized_input=normalized_input,
            triggered_rules=triggered_rules,
            missing_critical_data=missing_critical_data,
            output=output,
            protocol_metadata=protocol_metadata,
            clinical_use_status=clinical_use_status,
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    def get_for_tenant(
        self, session: Session, audit_id: str, tenant_id: str
    ) -> AuditEventModel | None:
        return (
            session.execute(
                select(AuditEventModel).where(
                    AuditEventModel.audit_id == audit_id,
                    AuditEventModel.tenant_id == tenant_id,
                )
            )
            .scalars()
            .first()
        )
