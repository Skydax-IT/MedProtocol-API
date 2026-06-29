from __future__ import annotations

from datetime import datetime
from typing import Any

from app.schemas.common import ResponseMeta, StrictBaseModel


class AuditEventResponse(StrictBaseModel):
    audit_id: str
    request_id: str
    tenant_id: str
    api_key_id: str
    external_encounter_id: str | None
    country_code: str
    module: str
    user_role: str
    input_summary: dict[str, Any]
    normalized_input: dict[str, Any]
    triggered_rules: list[str]
    missing_critical_data: list[str]
    output: dict[str, Any]
    protocol_metadata: dict[str, Any]
    clinical_use_status: str
    created_at: datetime
    meta: ResponseMeta
