from __future__ import annotations

from app.domain.next_question import NextQuestionEngine
from app.infrastructure.rules.loader import load_demo_catalog


def test_next_question_prioritizes_child_danger_sign() -> None:
    catalog = load_demo_catalog()
    result = NextQuestionEngine(catalog.questions).next_question(
        {
            "session_id": "sess_demo_001",
            "patient_context": {
                "age_months": 24,
                "sex": "female",
                "pregnancy_status": "not_applicable",
            },
            "encounter_context": {
                "country_code": "CF",
                "user_role": "community_health_worker",
                "language": "fr",
                "channel": "ussd",
            },
            "known_answers": {"main_complaint": "fever", "duration_days": 2},
        }
    )

    assert result.next_question is not None
    assert result.next_question.question_id == "child_danger_lethargy"
    assert result.missing_critical_data == ("danger_signs.lethargy_or_unconscious",)
