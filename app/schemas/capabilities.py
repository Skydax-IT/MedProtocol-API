from __future__ import annotations

from app.schemas.common import ResponseMeta, StrictBaseModel


class CapabilitiesResponse(StrictBaseModel):
    countries: list[str]
    modules: list[str]
    roles: list[str]
    languages: list[str]
    output_formats: list[str]
    clinical_use_status: str = "not_for_real_patient_care"
    meta: ResponseMeta
