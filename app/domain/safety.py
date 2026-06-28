from __future__ import annotations

from collections.abc import Iterable, Mapping

from app.domain.exceptions import SafetyViolationError
from app.domain.models import Rule

FORBIDDEN_RESULT_KEYS = {"medication", "dose", "dosage", "prescription", "diagnosis"}


class SafetyGuardrails:
    def validate_rules(self, rules: Iterable[Rule]) -> None:
        for rule in rules:
            self._validate_rule_status(rule)
            self._validate_rule_safety(rule)
            self._validate_result_payload(rule.result)

    def _validate_rule_status(self, rule: Rule) -> None:
        if rule.validation_status != "demo_only":
            raise SafetyViolationError(f"Rule {rule.rule_id} is not marked demo_only")
        if rule.status != "draft":
            raise SafetyViolationError(f"Rule {rule.rule_id} is not marked draft")
        if rule.clinical_use_status != "not_for_real_patient_care":
            raise SafetyViolationError(f"Rule {rule.rule_id} has unsafe clinical_use_status")
        if rule.real_care_validation_status != "not_validated_for_real_care":
            raise SafetyViolationError(
                f"Rule {rule.rule_id} is not marked not_validated_for_real_care"
            )

    def _validate_rule_safety(self, rule: Rule) -> None:
        if rule.safety.get("allow_medication") is not False:
            raise SafetyViolationError(f"Rule {rule.rule_id} does not forbid medication")
        if rule.safety.get("allow_dosage") is not False:
            raise SafetyViolationError(f"Rule {rule.rule_id} does not forbid dosage")
        if rule.safety.get("allow_diagnosis") is not False:
            raise SafetyViolationError(f"Rule {rule.rule_id} does not forbid diagnosis")

    def _validate_result_payload(self, payload: Mapping[str, object]) -> None:
        present = FORBIDDEN_RESULT_KEYS.intersection(payload.keys())
        if present:
            joined = ", ".join(sorted(present))
            raise SafetyViolationError(f"Forbidden clinical result keys present: {joined}")
