from __future__ import annotations

from app.domain.exceptions import UnsupportedRoleError
from app.domain.models import DecisionResult, ImmediateAction, ScopeProfile

ACTION_TO_SCOPE_CATEGORY = {
    "urgent_referral": "recommend_referral",
    "ask_missing_questions": "ask_missing_questions",
    "routine_guidance": "provide_simple_explanation",
}


class ScopeAdapter:
    def apply(self, result: DecisionResult, scope: ScopeProfile) -> DecisionResult:
        required_category = ACTION_TO_SCOPE_CATEGORY.get(
            result.immediate_action.category,
            result.immediate_action.category,
        )
        if required_category not in scope.allowed_action_categories:
            raise UnsupportedRoleError(
                f"Role {scope.role} is not allowed to receive action category {required_category}"
            )

        removed = tuple(
            sorted(
                set(result.forbidden_content_removed).union(
                    {"diagnosis", "prescription", "dosage", "medication"}
                )
            )
        )
        action = result.immediate_action
        if "diagnosis_confirmation" in scope.forbidden_action_categories:
            action = ImmediateAction(
                category=action.category,
                label=action.label,
                text=action.text.replace("évaluer", "faire évaluer"),
            )

        return DecisionResult(
            urgency_level=result.urgency_level,
            referral_required=result.referral_required,
            immediate_action=action,
            reason=result.reason,
            danger_signs_detected=result.danger_signs_detected,
            possible_suspicions=result.possible_suspicions,
            missing_critical_data=result.missing_critical_data,
            actions_to_avoid=result.actions_to_avoid,
            short_message=self._fit_sms(result.short_message, scope),
            explanation_for_worker=self._adapt_explanation(result.explanation_for_worker, scope),
            source=result.source,
            considered_rule_ids=result.considered_rule_ids,
            triggered_rule_ids=result.triggered_rule_ids,
            scope_role=scope.role,
            forbidden_content_removed=removed,
        )

    def _fit_sms(self, message: str, scope: ScopeProfile) -> str:
        limit = int(scope.output_constraints.get("max_sms_chars", 160))
        if len(message) <= limit:
            return message
        return message[: max(0, limit - 1)].rstrip() + "…"

    def _adapt_explanation(self, explanation: str, scope: ScopeProfile) -> str:
        if scope.role == "doctor":
            return (
                explanation
                + " La sortie reste limitée aux règles de démonstration explicitement encodées."
            )
        if scope.role == "midwife":
            return explanation.replace("travailleur", "professionnel de maternité")
        return explanation
