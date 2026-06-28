from __future__ import annotations

from datetime import UTC, datetime

from app.api.deps import enforce_tenant_country_module
from app.api.errors import forbidden
from app.application.services.serializers import (
    question_to_public_dict,
    rule_to_public_dict,
    scope_to_public_dict,
)
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.infrastructure.rules.loader import RuleCatalog, load_demo_catalog
from app.schemas.common import ResponseMeta
from app.schemas.offline import OfflineBundleResponse


class OfflineBundleService:
    def __init__(
        self,
        tenant: AuthenticatedTenant,
        request_id: str,
        catalog: RuleCatalog | None = None,
    ) -> None:
        self.tenant = tenant
        self.request_id = request_id
        self.catalog = catalog or load_demo_catalog()

    def get_bundle(self, country_code: str, module_code: str) -> OfflineBundleResponse:
        country_code = country_code.upper()
        enforce_tenant_country_module(
            self.tenant, country_code=country_code, module_code=module_code
        )
        country_pack = self.catalog.country_packs.get(country_code)
        if country_pack is None:
            raise forbidden("COUNTRY_NOT_ENABLED", f"Country {country_code} is not enabled.")
        if module_code not in country_pack.enabled_modules:
            raise forbidden("MODULE_NOT_ENABLED", f"Module {module_code} is not enabled.")
        rules = [
            rule for rule in self.catalog.rules if rule.module in {"general_triage", module_code}
        ]
        questions = [
            question for question in self.catalog.questions if question.module == module_code
        ]
        versions = sorted({rule.protocol_version for rule in rules})
        return OfflineBundleResponse(
            bundle_id=f"{country_code}-{module_code}-DEMO_DRAFT_NOT_VALIDATED",
            country_code=country_code,
            module_code=module_code,
            protocol_versions=versions,
            rules=[rule_to_public_dict(rule) for rule in rules],
            questions=[question_to_public_dict(question) for question in questions],
            scopes=[scope_to_public_dict(scope) for scope in self.catalog.scopes.values()],
            translations=[],
            clinical_use_status="not_for_real_patient_care",
            signature="demo-signature-placeholder",
            expires_at=datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC),
            meta=ResponseMeta(request_id=self.request_id, tenant_id=self.tenant.tenant_id),
        )
