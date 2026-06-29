from __future__ import annotations

from app.domain.models import Rule
from app.domain.rule_evaluator import RuleEvaluator


def make_rule(condition: dict[str, object]) -> Rule:
    return Rule(
        rule_id="rule_test",
        protocol_id="demo_general_triage",
        protocol_version="DEMO_DRAFT_NOT_VALIDATED",
        priority=1,
        module="general_triage",
        patient_group="general",
        validation_status="demo_only",
        clinical_use_status="not_for_real_patient_care",
        condition=condition,
        result={},
        safety={"allow_medication": False, "allow_dosage": False, "allow_diagnosis": False},
        status="draft",
        real_care_validation_status="not_validated_for_real_care",
    )


def test_rule_evaluator_supports_core_operators() -> None:
    evaluator = RuleEvaluator()
    payload = {"a": {"b": 3, "c": "x", "d": None}}

    assert evaluator.evaluate_rule(
        make_rule({"path": "a.b", "operator": "equals", "value": 3}), payload
    )
    assert evaluator.evaluate_rule(
        make_rule({"path": "a.b", "operator": "greater_than", "value": 2}), payload
    )
    assert evaluator.evaluate_rule(
        make_rule({"path": "a.c", "operator": "in", "value": ["x"]}), payload
    )
    assert evaluator.evaluate_rule(make_rule({"path": "a.d", "operator": "not_exists"}), payload)
    assert evaluator.evaluate_rule(
        make_rule({"path": "a.missing", "operator": "not_exists"}), payload
    )


def test_rule_evaluator_handles_nested_any_all() -> None:
    evaluator = RuleEvaluator()
    rule = make_rule(
        {
            "all": [
                {"path": "age", "operator": "greater_or_equal", "value": 0},
                {
                    "any": [
                        {"path": "danger.convulsions", "operator": "equals", "value": True},
                        {"path": "danger.lethargy", "operator": "equals", "value": True},
                    ]
                },
            ]
        }
    )
    assert evaluator.evaluate_rule(rule, {"age": 24, "danger": {"lethargy": True}})
