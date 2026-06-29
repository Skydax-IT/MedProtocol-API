from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.domain.rule_evaluator import MISSING, get_path_value


class MissingDataDetector:
    GENERAL_REQUIRED: tuple[tuple[str, str], ...] = (
        ("patient_context.age_months", "age_months"),
        ("encounter_context.country_code", "country_code"),
        ("encounter_context.user_role", "user_role"),
    )
    CHILD_REQUIRED: tuple[tuple[str, str], ...] = (
        ("patient_context.weight_kg", "weight_kg"),
        ("clinical_inputs.vitals.respiratory_rate", "respiratory_rate"),
        ("clinical_inputs.danger_signs.convulsions", "danger_signs.convulsions"),
        (
            "clinical_inputs.danger_signs.lethargy_or_unconscious",
            "danger_signs.lethargy_or_unconscious",
        ),
        (
            "clinical_inputs.danger_signs.unable_to_drink_or_breastfeed",
            "danger_signs.unable_to_drink_or_breastfeed",
        ),
    )
    PREGNANCY_REQUIRED: tuple[tuple[str, str], ...] = (
        ("clinical_inputs.danger_signs.severe_bleeding", "danger_signs.severe_bleeding"),
        ("clinical_inputs.danger_signs.convulsions", "danger_signs.convulsions"),
        (
            "clinical_inputs.danger_signs.severe_abdominal_pain",
            "danger_signs.severe_abdominal_pain",
        ),
        (
            "clinical_inputs.danger_signs.severe_headache_or_visual_disturbance",
            "danger_signs.severe_headache_or_visual_disturbance",
        ),
    )

    def detect(self, payload: Mapping[str, Any]) -> tuple[str, ...]:
        missing: list[str] = []
        self._append_missing(payload, self.GENERAL_REQUIRED, missing)

        age_months = get_path_value(payload, "patient_context.age_months")
        pregnancy_status = get_path_value(payload, "patient_context.pregnancy_status")
        if isinstance(age_months, int) and 0 <= age_months <= 59:
            self._append_missing(payload, self.CHILD_REQUIRED, missing)
        if pregnancy_status == "pregnant":
            self._append_missing(payload, self.PREGNANCY_REQUIRED, missing)

        return tuple(dict.fromkeys(missing))

    def _append_missing(
        self,
        payload: Mapping[str, Any],
        required: tuple[tuple[str, str], ...],
        missing: list[str],
    ) -> None:
        for path, label in required:
            value = get_path_value(payload, path)
            if value is MISSING or value is None:
                missing.append(label)
