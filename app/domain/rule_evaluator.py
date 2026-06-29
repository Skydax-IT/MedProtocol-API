from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.domain.exceptions import RuleEvaluationError
from app.domain.models import Rule

MISSING = object()


def get_path_value(payload: Mapping[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
            continue
        return MISSING
    return current


class RuleEvaluator:
    def evaluate_rule(self, rule: Rule, payload: Mapping[str, Any]) -> bool:
        return self.evaluate_condition(rule.condition, payload)

    def evaluate_condition(self, condition: Mapping[str, Any], payload: Mapping[str, Any]) -> bool:
        if "all" in condition:
            children = condition["all"]
            if not isinstance(children, list):
                raise RuleEvaluationError("all condition must contain a list")
            return all(self.evaluate_condition(child, payload) for child in children)

        if "any" in condition:
            children = condition["any"]
            if not isinstance(children, list):
                raise RuleEvaluationError("any condition must contain a list")
            return any(self.evaluate_condition(child, payload) for child in children)

        path = condition.get("path")
        operator = condition.get("operator")
        expected = condition.get("value")
        if not isinstance(path, str) or not isinstance(operator, str):
            raise RuleEvaluationError("leaf condition requires path and operator")

        actual = get_path_value(payload, path)
        return self._compare(actual=actual, operator=operator, expected=expected)

    def _compare(self, actual: Any, operator: str, expected: Any) -> bool:
        if operator == "exists":
            return actual is not MISSING and actual is not None
        if operator == "not_exists":
            return actual is MISSING or actual is None
        if actual is MISSING:
            return operator in {"not_equals", "not_in"}

        if operator == "equals":
            return actual == expected
        if operator == "not_equals":
            return actual != expected
        if operator == "in":
            return actual in self._ensure_collection(expected)
        if operator == "not_in":
            return actual not in self._ensure_collection(expected)
        if operator == "greater_than":
            return self._ordered(actual, expected, lambda left, right: left > right)
        if operator == "greater_or_equal":
            return self._ordered(actual, expected, lambda left, right: left >= right)
        if operator == "less_than":
            return self._ordered(actual, expected, lambda left, right: left < right)
        if operator == "less_or_equal":
            return self._ordered(actual, expected, lambda left, right: left <= right)
        raise RuleEvaluationError(f"Unsupported operator: {operator}")

    def _ensure_collection(self, value: Any) -> tuple[Any, ...]:
        if isinstance(value, (list, tuple, set, frozenset)):
            return tuple(value)
        raise RuleEvaluationError("in/not_in operator requires a collection value")

    def _ordered(self, actual: Any, expected: Any, comparator: Any) -> bool:
        if actual is None or expected is None:
            return False
        try:
            return bool(comparator(actual, expected))
        except TypeError as exc:
            raise RuleEvaluationError("ordered comparison received incompatible values") from exc
