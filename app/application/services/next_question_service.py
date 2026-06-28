from __future__ import annotations

from app.api.deps import enforce_tenant_country_module
from app.domain.next_question import NextQuestionEngine
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.infrastructure.rules.loader import RuleCatalog, load_demo_catalog
from app.schemas.common import ResponseMeta
from app.schemas.triage import (
    NextQuestionRequest,
    NextQuestionResponse,
    NextQuestionResponseItem,
)


class NextQuestionService:
    def __init__(
        self,
        tenant: AuthenticatedTenant,
        request_id: str,
        catalog: RuleCatalog | None = None,
    ) -> None:
        self.tenant = tenant
        self.request_id = request_id
        self.catalog = catalog or load_demo_catalog()

    def next_question(self, request: NextQuestionRequest) -> NextQuestionResponse:
        payload = request.model_dump(mode="json")
        country_code = payload["encounter_context"]["country_code"].upper()
        module_code = self._determine_module(payload)
        enforce_tenant_country_module(
            self.tenant, country_code=country_code, module_code=module_code
        )

        result = NextQuestionEngine(self.catalog.questions).next_question(payload)
        language = payload["encounter_context"].get("language", "fr")
        item = None
        if result.next_question is not None:
            item = NextQuestionResponseItem(
                question_id=result.next_question.question_id,
                text=result.next_question.text.get(language, result.next_question.text["fr"]),
                answer_type=result.next_question.answer_type,
                priority=result.next_question.priority,
                reason="Question prioritaire de signes de danger.",
                clinical_use_status=result.next_question.clinical_use_status,
            )
        return NextQuestionResponse(
            session_id=result.session_id,
            next_question=item,
            can_evaluate_now=result.can_evaluate_now,
            missing_critical_data=list(result.missing_critical_data),
            meta=ResponseMeta(request_id=self.request_id, tenant_id=self.tenant.tenant_id),
        )

    def _determine_module(self, payload: dict[str, object]) -> str:
        patient_context = payload["patient_context"]
        if (
            isinstance(patient_context, dict)
            and patient_context.get("pregnancy_status") == "pregnant"
        ):
            return "pregnancy_triage"
        age_months = (
            patient_context.get("age_months") if isinstance(patient_context, dict) else None
        )
        if isinstance(age_months, int) and 0 <= age_months <= 59:
            return "child_triage"
        return "general_triage"
