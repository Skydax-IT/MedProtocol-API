from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.domain.exceptions import UnsupportedCountryError, UnsupportedRoleError
from app.domain.missing_data import MissingDataDetector
from app.domain.models import CountryPack, DecisionResult, ProtocolMetadata, Rule, ScopeProfile
from app.domain.output_composer import OutputComposer
from app.domain.rule_evaluator import RuleEvaluator
from app.domain.safety import SafetyGuardrails
from app.domain.scope import ScopeAdapter


class DecisionEngine:
    def __init__(
        self,
        rules: Sequence[Rule],
        protocols: Mapping[str, ProtocolMetadata],
        country_packs: Mapping[str, CountryPack],
        scopes: Mapping[str, ScopeProfile],
    ) -> None:
        self.rules = tuple(rules)
        self.protocols = dict(protocols)
        self.country_packs = dict(country_packs)
        self.scopes = dict(scopes)
        self.evaluator = RuleEvaluator()
        self.missing_data = MissingDataDetector()
        self.composer = OutputComposer()
        self.scope_adapter = ScopeAdapter()
        self.safety = SafetyGuardrails()
        self.safety.validate_rules(self.rules)

    def evaluate(self, payload: Mapping[str, Any]) -> DecisionResult:
        country_code = self._get_country_code(payload)
        country_pack = self.country_packs.get(country_code)
        if country_pack is None:
            raise UnsupportedCountryError(f"Country {country_code} is not enabled")

        role = self._get_role(payload)
        scope = self.scopes.get(role)
        if scope is None:
            raise UnsupportedRoleError(f"Role {role} is not enabled")

        applicable_rules = self._applicable_rules(country_pack)
        considered_rule_ids = tuple(rule.rule_id for rule in applicable_rules)
        triggered_rules = [
            rule for rule in applicable_rules if self.evaluator.evaluate_rule(rule, payload)
        ]
        missing = self.missing_data.detect(payload)
        urgent_triggered = any(
            rule.result.get("urgency_level") == "urgent_referral" for rule in triggered_rules
        )

        if (
            missing
            and not urgent_triggered
            and not any(rule.rule_id == "demo_insufficient_data_001" for rule in triggered_rules)
        ):
            fallback = self._find_rule("demo_insufficient_data_001")
            if fallback:
                triggered_rules.append(fallback)
        if (
            not missing
            and not urgent_triggered
            and not any(
                rule.rule_id == "demo_general_no_demo_danger_001" for rule in triggered_rules
            )
        ):
            fallback = self._find_rule("demo_general_no_demo_danger_001")
            if fallback:
                triggered_rules.append(fallback)

        triggered_rules = self._sort_rules(triggered_rules)
        result = self.composer.compose(
            payload=payload,
            triggered_rules=triggered_rules,
            considered_rule_ids=considered_rule_ids,
            missing_critical_data=missing,
            country_pack=country_pack,
            protocols=self.protocols,
        )
        return self.scope_adapter.apply(result, scope)

    def _applicable_rules(self, country_pack: CountryPack) -> tuple[Rule, ...]:
        enabled = set(country_pack.enabled_modules)
        rules = [
            rule
            for rule in self.rules
            if rule.module in enabled and rule.rule_id != "demo_general_no_demo_danger_001"
        ]
        return self._sort_rules(rules)

    def _sort_rules(self, rules: Sequence[Rule]) -> tuple[Rule, ...]:
        return tuple(sorted(rules, key=lambda rule: (-rule.priority, rule.rule_id)))

    def _find_rule(self, rule_id: str) -> Rule | None:
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    def _get_country_code(self, payload: Mapping[str, Any]) -> str:
        encounter = payload.get("encounter_context", {})
        country_code = encounter.get("country_code") if isinstance(encounter, dict) else None
        if not isinstance(country_code, str) or not country_code:
            raise UnsupportedCountryError("country_code is required")
        return country_code.upper()

    def _get_role(self, payload: Mapping[str, Any]) -> str:
        encounter = payload.get("encounter_context", {})
        role = encounter.get("user_role") if isinstance(encounter, dict) else None
        if not isinstance(role, str) or not role:
            raise UnsupportedRoleError("user_role is required")
        return role
