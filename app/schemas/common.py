from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ResponseMeta(StrictBaseModel):
    request_id: str
    tenant_id: str
    api_version: str = "v1"
    clinical_use_status: str = "not_for_real_patient_care"


class SourceMetadataResponse(StrictBaseModel):
    protocol_id: str
    protocol_version: str
    rule_ids: list[str]
    validation_status: str = "demo_only"
    clinical_use_status: str = "not_for_real_patient_care"
    real_care_validation_status: str = "not_validated_for_real_care"


class ImmediateActionResponse(StrictBaseModel):
    category: str
    label: str
    text: str


class HealthResponse(StrictBaseModel):
    status: str
    service: str
    timestamp: str


class ReadinessResponse(StrictBaseModel):
    status: str
    service: str
    environment: str
    checks: dict[str, str]


class VersionResponse(StrictBaseModel):
    service: str
    version: str
    commit: str
    environment: str


class PseudonymousReferenceMixin(BaseModel):
    patient_ref: str | None = Field(
        default=None,
        max_length=128,
        description="Optional external pseudonymous reference. Do not send direct identifiers.",
    )
