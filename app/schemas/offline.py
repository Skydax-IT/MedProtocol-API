from __future__ import annotations

from datetime import datetime
from typing import Any

from app.schemas.common import ResponseMeta, StrictBaseModel


class OfflineBundleResponse(StrictBaseModel):
    bundle_id: str
    country_code: str
    module_code: str
    protocol_versions: list[str]
    rules: list[dict[str, Any]]
    questions: list[dict[str, Any]]
    scopes: list[dict[str, Any]]
    translations: list[dict[str, Any]]
    clinical_use_status: str = "not_for_real_patient_care"
    signature: str
    expires_at: datetime
    meta: ResponseMeta
