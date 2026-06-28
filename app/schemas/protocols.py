from __future__ import annotations

from app.schemas.common import StrictBaseModel


class ProtocolSummary(StrictBaseModel):
    protocol_id: str
    title: str
    module: str
    version: str
    status: str
    validation_status: str
    clinical_use_status: str
    real_care_validation_status: str


class ProtocolListResponse(StrictBaseModel):
    items: list[ProtocolSummary]


class ProtocolDetailResponse(ProtocolSummary):
    source_label: str
    country_code: str | None
    effective_from: str | None
    deprecated_at: str | None
    rule_ids: list[str]
