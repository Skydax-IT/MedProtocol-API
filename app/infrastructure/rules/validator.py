from __future__ import annotations

from app.domain.safety import SafetyGuardrails
from app.infrastructure.rules.loader import RuleCatalog


def validate_catalog(catalog: RuleCatalog) -> None:
    SafetyGuardrails().validate_rules(catalog.rules)
    for protocol in catalog.protocols.values():
        if protocol.validation_status != "demo_only":
            raise ValueError(f"Protocol {protocol.protocol_id} is not demo_only")
        if protocol.clinical_use_status != "not_for_real_patient_care":
            raise ValueError(f"Protocol {protocol.protocol_id} has unsafe clinical_use_status")
        if protocol.real_care_validation_status != "not_validated_for_real_care":
            raise ValueError(
                f"Protocol {protocol.protocol_id} is not marked not_validated_for_real_care"
            )
