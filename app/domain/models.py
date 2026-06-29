from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

DEMO_PROTOCOL_VERSION = "DEMO_DRAFT_NOT_VALIDATED"
DEMO_VALIDATION_STATUS = "demo_only"
DEMO_CLINICAL_USE_STATUS = "not_for_real_patient_care"
DEMO_REAL_CARE_VALIDATION_STATUS = "not_validated_for_real_care"


@dataclass(frozen=True)
class ProtocolMetadata:
    protocol_id: str
    title: str
    module: str
    version: str
    status: str
    validation_status: str
    clinical_use_status: str
    real_care_validation_status: str
    source_label: str
    country_code: str | None = None
    effective_from: str | None = None
    deprecated_at: str | None = None


@dataclass(frozen=True)
class Rule:
    rule_id: str
    protocol_id: str
    protocol_version: str
    priority: int
    module: str
    patient_group: str
    validation_status: str
    clinical_use_status: str
    condition: Mapping[str, Any]
    result: Mapping[str, Any]
    safety: Mapping[str, Any]
    status: str = "draft"
    real_care_validation_status: str = DEMO_REAL_CARE_VALIDATION_STATUS


@dataclass(frozen=True)
class CountryPack:
    country_code: str
    country_name: str
    status: str
    languages: tuple[str, ...]
    enabled_modules: tuple[str, ...]
    clinical_use_status: str
    referral_wording: Mapping[str, str]
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ScopeProfile:
    role: str
    display_name: str
    allowed_action_categories: tuple[str, ...]
    forbidden_action_categories: tuple[str, ...]
    output_constraints: Mapping[str, Any]


@dataclass(frozen=True)
class Question:
    question_id: str
    module: str
    priority: int
    applies_when: Mapping[str, Any]
    text: Mapping[str, str]
    answer_type: str
    maps_to: str
    clinical_use_status: str


@dataclass(frozen=True)
class SourceMetadata:
    protocol_id: str
    protocol_version: str
    rule_ids: tuple[str, ...]
    validation_status: str
    clinical_use_status: str
    real_care_validation_status: str = DEMO_REAL_CARE_VALIDATION_STATUS


@dataclass(frozen=True)
class ImmediateAction:
    category: str
    label: str
    text: str


@dataclass(frozen=True)
class DecisionResult:
    urgency_level: str
    referral_required: bool | None
    immediate_action: ImmediateAction
    reason: str
    danger_signs_detected: tuple[str, ...]
    possible_suspicions: tuple[str, ...]
    missing_critical_data: tuple[str, ...]
    actions_to_avoid: tuple[str, ...]
    short_message: str
    explanation_for_worker: str
    source: SourceMetadata
    considered_rule_ids: tuple[str, ...]
    triggered_rule_ids: tuple[str, ...]
    scope_role: str
    forbidden_content_removed: tuple[str, ...]
