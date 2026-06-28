from __future__ import annotations

from app.domain.engine import DecisionEngine
from app.infrastructure.rules.loader import load_demo_catalog


def test_engine_detects_child_danger_signs(child_danger_payload: dict[str, object]) -> None:
    catalog = load_demo_catalog()
    result = DecisionEngine(
        rules=catalog.rules,
        protocols=catalog.protocols,
        country_packs=catalog.country_packs,
        scopes=catalog.scopes,
    ).evaluate(child_danger_payload)

    assert result.urgency_level == "urgent_referral"
    assert result.referral_required is True
    assert result.source.rule_ids == ("demo_child_danger_001",)
    assert result.source.validation_status == "demo_only"
    assert result.source.clinical_use_status == "not_for_real_patient_care"
    assert "lethargy_or_unconscious" in result.danger_signs_detected
    assert "respiratory_rate" in result.missing_critical_data


def test_engine_is_deterministic(child_danger_payload: dict[str, object]) -> None:
    catalog = load_demo_catalog()
    engine = DecisionEngine(
        rules=catalog.rules,
        protocols=catalog.protocols,
        country_packs=catalog.country_packs,
        scopes=catalog.scopes,
    )
    first = engine.evaluate(child_danger_payload)
    second = engine.evaluate(child_danger_payload)

    assert first == second
