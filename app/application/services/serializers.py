from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.domain.models import DecisionResult, ProtocolMetadata, Question, Rule, ScopeProfile


def decision_to_payload(result: DecisionResult) -> dict[str, Any]:
    source = asdict(result.source)
    source["rule_ids"] = list(result.source.rule_ids)
    return {
        "urgency_level": result.urgency_level,
        "referral_required": result.referral_required,
        "immediate_action": asdict(result.immediate_action),
        "reason": result.reason,
        "danger_signs_detected": list(result.danger_signs_detected),
        "possible_suspicions": list(result.possible_suspicions),
        "missing_critical_data": list(result.missing_critical_data),
        "actions_to_avoid": list(result.actions_to_avoid),
        "short_message": result.short_message,
        "explanation_for_worker": result.explanation_for_worker,
        "source": source,
    }


def protocol_to_summary(protocol: ProtocolMetadata) -> dict[str, Any]:
    return {
        "protocol_id": protocol.protocol_id,
        "title": protocol.title,
        "module": protocol.module,
        "version": protocol.version,
        "status": protocol.status,
        "validation_status": protocol.validation_status,
        "clinical_use_status": protocol.clinical_use_status,
        "real_care_validation_status": protocol.real_care_validation_status,
    }


def protocol_to_detail(protocol: ProtocolMetadata, rule_ids: list[str]) -> dict[str, Any]:
    payload = protocol_to_summary(protocol)
    payload.update(
        {
            "source_label": protocol.source_label,
            "country_code": protocol.country_code,
            "effective_from": protocol.effective_from,
            "deprecated_at": protocol.deprecated_at,
            "rule_ids": rule_ids,
        }
    )
    return payload


def rule_to_public_dict(rule: Rule) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "protocol_id": rule.protocol_id,
        "protocol_version": rule.protocol_version,
        "priority": rule.priority,
        "module": rule.module,
        "patient_group": rule.patient_group,
        "status": rule.status,
        "validation_status": rule.validation_status,
        "clinical_use_status": rule.clinical_use_status,
        "real_care_validation_status": rule.real_care_validation_status,
        "condition": rule.condition,
        "result": rule.result,
        "safety": rule.safety,
    }


def question_to_public_dict(question: Question) -> dict[str, Any]:
    return {
        "question_id": question.question_id,
        "module": question.module,
        "priority": question.priority,
        "applies_when": question.applies_when,
        "text": question.text,
        "answer_type": question.answer_type,
        "maps_to": question.maps_to,
        "clinical_use_status": question.clinical_use_status,
    }


def scope_to_public_dict(scope: ScopeProfile) -> dict[str, Any]:
    return {
        "role": scope.role,
        "display_name": scope.display_name,
        "allowed_action_categories": list(scope.allowed_action_categories),
        "forbidden_action_categories": list(scope.forbidden_action_categories),
        "output_constraints": dict(scope.output_constraints),
    }
