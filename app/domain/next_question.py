from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from app.domain.models import Question


@dataclass(frozen=True)
class NextQuestionResult:
    session_id: str
    next_question: Question | None
    can_evaluate_now: bool
    missing_critical_data: tuple[str, ...]


class NextQuestionEngine:
    def __init__(self, questions: Sequence[Question]) -> None:
        self.questions = tuple(
            sorted(questions, key=lambda item: (-item.priority, item.question_id))
        )

    def next_question(self, payload: Mapping[str, Any]) -> NextQuestionResult:
        session_id = str(payload.get("session_id", ""))
        known_answers = payload.get("known_answers", {})
        if not isinstance(known_answers, Mapping):
            known_answers = {}

        patient_context = payload.get("patient_context", {})
        pregnancy_status = (
            patient_context.get("pregnancy_status")
            if isinstance(patient_context, Mapping)
            else None
        )
        age_months = (
            patient_context.get("age_months") if isinstance(patient_context, Mapping) else None
        )
        patient_groups = self._patient_groups(age_months, pregnancy_status)

        candidates = [
            question
            for question in self.questions
            if self._applies(question, patient_groups)
            and not self._is_answered(question, known_answers)
        ]
        if candidates:
            question = candidates[0]
            return NextQuestionResult(
                session_id=session_id,
                next_question=question,
                can_evaluate_now=False,
                missing_critical_data=(self._missing_label(question.maps_to),),
            )
        return NextQuestionResult(
            session_id=session_id,
            next_question=None,
            can_evaluate_now=True,
            missing_critical_data=(),
        )

    def _patient_groups(self, age_months: object, pregnancy_status: object) -> tuple[str, ...]:
        groups = ["general"]
        if isinstance(age_months, int) and 0 <= age_months <= 59:
            groups.append("child_0_59_months")
        if pregnancy_status == "pregnant":
            groups.append("pregnant_person")
        return tuple(groups)

    def _applies(self, question: Question, patient_groups: Sequence[str]) -> bool:
        group = question.applies_when.get("patient_group")
        return group in patient_groups

    def _is_answered(self, question: Question, known_answers: Mapping[str, Any]) -> bool:
        keys = {
            question.maps_to,
            question.maps_to.replace("clinical_inputs.", ""),
            question.maps_to.split(".")[-1],
        }
        return any(key in known_answers and known_answers[key] is not None for key in keys)

    def _missing_label(self, maps_to: str) -> str:
        return maps_to.replace("clinical_inputs.", "")
