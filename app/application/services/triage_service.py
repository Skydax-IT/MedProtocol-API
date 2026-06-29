from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.api.deps import enforce_tenant_country_module
from app.application.services.serializers import decision_to_payload
from app.domain.engine import DecisionEngine
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.infrastructure.repositories.audit_repository import AuditRepository
from app.infrastructure.rules.loader import RuleCatalog, load_demo_catalog
from app.schemas.common import ResponseMeta
from app.schemas.triage import TriageEvaluateRequest, TriageEvaluateResponse


class TriageEvaluationService:
    def __init__(
        self,
        session: Session,
        tenant: AuthenticatedTenant,
        request_id: str,
        catalog: RuleCatalog | None = None,
    ) -> None:
        self.session = session
        self.tenant = tenant
        self.request_id = request_id
        self.catalog = catalog or load_demo_catalog()
        self.audit_repository = AuditRepository()

    def evaluate(self, request: TriageEvaluateRequest) -> TriageEvaluateResponse:
        payload = request.model_dump(mode="json")
        payload["encounter_context"]["country_code"] = payload["encounter_context"][
            "country_code"
        ].upper()
        module = self._determine_module(payload)
        enforce_tenant_country_module(
            self.tenant,
            country_code=payload["encounter_context"]["country_code"],
            module_code=module,
        )

        engine = DecisionEngine(
            rules=self.catalog.rules,
            protocols=self.catalog.protocols,
            country_packs=self.catalog.country_packs,
            scopes=self.catalog.scopes,
        )
        result = engine.evaluate(payload)
        decision_payload = decision_to_payload(result)
        source = decision_payload["source"]

        audit = self.audit_repository.create(
            self.session,
            tenant_id=self.tenant.tenant_id,
            api_key_id=self.tenant.api_key_id,
            request_id=self.request_id,
            external_encounter_id=payload["client_context"].get("external_encounter_id"),
            country_code=payload["encounter_context"]["country_code"],
            module=self.catalog.protocols[source["protocol_id"]].module,
            user_role=payload["encounter_context"]["user_role"],
            input_summary=self._input_summary(payload, module),
            normalized_input=self._minimized_input(payload),
            triggered_rules=list(result.triggered_rule_ids),
            missing_critical_data=list(result.missing_critical_data),
            output=decision_payload,
            protocol_metadata=source,
            clinical_use_status=source["clinical_use_status"],
        )

        response_payload: dict[str, Any] = {
            "audit_id": audit.audit_id,
            **decision_payload,
            "meta": ResponseMeta(
                request_id=self.request_id,
                tenant_id=self.tenant.tenant_id,
            ).model_dump(mode="json"),
        }
        return TriageEvaluateResponse.model_validate(response_payload)

    def _determine_module(self, payload: dict[str, Any]) -> str:
        patient_context = payload["patient_context"]
        if patient_context.get("pregnancy_status") == "pregnant":
            return "pregnancy_triage"
        age_months = patient_context.get("age_months")
        if isinstance(age_months, int) and 0 <= age_months <= 59:
            return "child_triage"
        return "general_triage"

    def _input_summary(self, payload: dict[str, Any], module: str) -> dict[str, Any]:
        danger_signs = payload["clinical_inputs"].get("danger_signs", {})
        detected = sorted(key for key, value in danger_signs.items() if value is True)
        return {
            "module": module,
            "age_months": payload["patient_context"].get("age_months"),
            "sex": payload["patient_context"].get("sex"),
            "pregnancy_status": payload["patient_context"].get("pregnancy_status"),
            "country_code": payload["encounter_context"].get("country_code"),
            "user_role": payload["encounter_context"].get("user_role"),
            "danger_signs_true": detected,
            "has_patient_ref": bool(payload["patient_context"].get("patient_ref")),
        }

    def _minimized_input(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "patient_context": payload["patient_context"],
            "encounter_context": payload["encounter_context"],
            "clinical_inputs": payload["clinical_inputs"],
            "resources_available": payload["resources_available"],
            "client_context": {
                "external_encounter_id": payload["client_context"].get("external_encounter_id"),
                "channel": payload["client_context"].get("channel"),
                "client_timestamp": payload["client_context"].get("client_timestamp"),
            },
        }
