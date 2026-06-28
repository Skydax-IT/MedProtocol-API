from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from app.domain.models import CountryPack, ProtocolMetadata, Question, Rule, ScopeProfile

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "demo"


@dataclass(frozen=True)
class RuleCatalog:
    protocols: dict[str, ProtocolMetadata]
    rules: tuple[Rule, ...]
    country_packs: dict[str, CountryPack]
    scopes: dict[str, ScopeProfile]
    questions: tuple[Question, ...]


@lru_cache(maxsize=1)
def load_demo_catalog() -> RuleCatalog:
    protocols = {
        protocol.protocol_id: protocol
        for protocol in _load_many(DATA_DIR / "protocols", _parse_protocol)
    }
    rules = tuple(_load_many(DATA_DIR / "rules", _parse_rule))
    country_packs = {
        pack.country_code: pack
        for pack in _load_many(DATA_DIR / "country_packs", _parse_country_pack)
    }
    scopes = {scope.role: scope for scope in _load_many(DATA_DIR / "scopes", _parse_scope)}
    questions = tuple(_load_many(DATA_DIR / "questions", _parse_question))
    return RuleCatalog(
        protocols=protocols,
        rules=tuple(sorted(rules, key=lambda rule: (-rule.priority, rule.rule_id))),
        country_packs=country_packs,
        scopes=scopes,
        questions=tuple(sorted(questions, key=lambda item: (-item.priority, item.question_id))),
    )


def _load_many(directory: Path, parser: Any) -> list[Any]:
    items: list[Any] = []
    for path in sorted(directory.glob("*.yaml")):
        loaded = _read_yaml(path)
        if isinstance(loaded, list):
            items.extend(parser(item) for item in loaded)
        else:
            items.append(parser(loaded))
    return items


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _parse_protocol(data: dict[str, Any]) -> ProtocolMetadata:
    return ProtocolMetadata(
        protocol_id=data["protocol_id"],
        title=data["title"],
        module=data["module"],
        version=data["version"],
        status=data["status"],
        validation_status=data["validation_status"],
        clinical_use_status=data["clinical_use_status"],
        real_care_validation_status=data.get(
            "real_care_validation_status",
            "not_validated_for_real_care",
        ),
        source_label=data["source_label"],
        country_code=data.get("country_code"),
        effective_from=str(data.get("effective_from")) if data.get("effective_from") else None,
        deprecated_at=data.get("deprecated_at"),
    )


def _parse_rule(data: dict[str, Any]) -> Rule:
    return Rule(
        rule_id=data["rule_id"],
        protocol_id=data["protocol_id"],
        protocol_version=data["protocol_version"],
        priority=int(data["priority"]),
        module=data["module"],
        patient_group=data.get("patient_group", "general"),
        validation_status=data["validation_status"],
        clinical_use_status=data["clinical_use_status"],
        condition=data["condition"],
        result=data["result"],
        safety=data["safety"],
        status=data.get("status", "draft"),
        real_care_validation_status=data.get(
            "real_care_validation_status",
            "not_validated_for_real_care",
        ),
    )


def _parse_country_pack(data: dict[str, Any]) -> CountryPack:
    return CountryPack(
        country_code=data["country_code"],
        country_name=data["country_name"],
        status=data["status"],
        languages=tuple(data["languages"]),
        enabled_modules=tuple(data["enabled_modules"]),
        clinical_use_status=data["clinical_use_status"],
        referral_wording=data["referral_wording"],
        notes=tuple(data.get("notes", [])),
    )


def _parse_scope(data: dict[str, Any]) -> ScopeProfile:
    return ScopeProfile(
        role=data["role"],
        display_name=data["display_name"],
        allowed_action_categories=tuple(data["allowed_action_categories"]),
        forbidden_action_categories=tuple(data["forbidden_action_categories"]),
        output_constraints=data.get("output_constraints", {}),
    )


def _parse_question(data: dict[str, Any]) -> Question:
    return Question(
        question_id=data["question_id"],
        module=data["module"],
        priority=int(data["priority"]),
        applies_when=data["applies_when"],
        text=data["text"],
        answer_type=data["answer_type"],
        maps_to=data["maps_to"],
        clinical_use_status=data["clinical_use_status"],
    )
