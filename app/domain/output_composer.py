from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.domain.models import (
    DEMO_CLINICAL_USE_STATUS,
    DEMO_PROTOCOL_VERSION,
    DEMO_REAL_CARE_VALIDATION_STATUS,
    DEMO_VALIDATION_STATUS,
    CountryPack,
    DecisionResult,
    ImmediateAction,
    ProtocolMetadata,
    Rule,
    SourceMetadata,
)

DANGER_SIGN_LABELS_FR = {
    "convulsions": "convulsions",
    "lethargy_or_unconscious": "léthargie/inconscience",
    "unable_to_drink_or_breastfeed": "incapacité à boire/téter",
    "respiratory_distress": "détresse respiratoire",
    "severe_bleeding": "saignement sévère",
    "severe_abdominal_pain": "douleur abdominale sévère",
    "severe_headache_or_visual_disturbance": "céphalées sévères ou troubles visuels",
}


class OutputComposer:
    def compose(
        self,
        payload: Mapping[str, Any],
        triggered_rules: Sequence[Rule],
        considered_rule_ids: Sequence[str],
        missing_critical_data: Sequence[str],
        country_pack: CountryPack,
        protocols: Mapping[str, ProtocolMetadata],
    ) -> DecisionResult:
        danger_signs = self._danger_signs_detected(payload)
        primary_rule = self._select_primary_rule(
            triggered_rules, missing_critical_data, danger_signs
        )
        source = self._source_metadata(primary_rule, triggered_rules, protocols)

        if primary_rule and primary_rule.result.get("urgency_level") == "urgent_referral":
            result = self._urgent_result(
                primary_rule=primary_rule,
                triggered_rules=triggered_rules,
                considered_rule_ids=considered_rule_ids,
                missing_critical_data=missing_critical_data,
                danger_signs=danger_signs,
                country_pack=country_pack,
                source=source,
            )
        elif missing_critical_data:
            result = self._cannot_determine_result(
                triggered_rules=triggered_rules,
                considered_rule_ids=considered_rule_ids,
                missing_critical_data=missing_critical_data,
                source=source,
            )
        else:
            result = self._routine_demo_result(
                triggered_rules=triggered_rules,
                considered_rule_ids=considered_rule_ids,
                source=source,
            )
        return result

    def _select_primary_rule(
        self,
        triggered_rules: Sequence[Rule],
        missing_critical_data: Sequence[str],
        danger_signs: Sequence[str],
    ) -> Rule | None:
        urgent_rules = [
            rule
            for rule in triggered_rules
            if rule.result.get("urgency_level") == "urgent_referral"
        ]
        if urgent_rules:
            return urgent_rules[0]
        if missing_critical_data:
            for rule in triggered_rules:
                if rule.rule_id == "demo_insufficient_data_001":
                    return rule
        for rule in triggered_rules:
            if rule.rule_id == "demo_general_no_demo_danger_001" and not danger_signs:
                return rule
        return triggered_rules[0] if triggered_rules else None

    def _source_metadata(
        self,
        primary_rule: Rule | None,
        triggered_rules: Sequence[Rule],
        protocols: Mapping[str, ProtocolMetadata],
    ) -> SourceMetadata:
        if primary_rule is None:
            return SourceMetadata(
                protocol_id="demo_general_triage",
                protocol_version=DEMO_PROTOCOL_VERSION,
                rule_ids=("demo_general_no_demo_danger_001",),
                validation_status=DEMO_VALIDATION_STATUS,
                clinical_use_status=DEMO_CLINICAL_USE_STATUS,
                real_care_validation_status=DEMO_REAL_CARE_VALIDATION_STATUS,
            )
        protocol = protocols.get(primary_rule.protocol_id)
        validation_status = (
            protocol.validation_status if protocol else primary_rule.validation_status
        )
        clinical_use_status = (
            protocol.clinical_use_status if protocol else primary_rule.clinical_use_status
        )
        real_care_validation_status = (
            protocol.real_care_validation_status
            if protocol
            else primary_rule.real_care_validation_status
        )
        rule_ids = tuple(rule.rule_id for rule in triggered_rules) or (primary_rule.rule_id,)
        return SourceMetadata(
            protocol_id=primary_rule.protocol_id,
            protocol_version=primary_rule.protocol_version,
            rule_ids=rule_ids,
            validation_status=validation_status,
            clinical_use_status=clinical_use_status,
            real_care_validation_status=real_care_validation_status,
        )

    def _urgent_result(
        self,
        primary_rule: Rule,
        triggered_rules: Sequence[Rule],
        considered_rule_ids: Sequence[str],
        missing_critical_data: Sequence[str],
        danger_signs: Sequence[str],
        country_pack: CountryPack,
        source: SourceMetadata,
    ) -> DecisionResult:
        labels = [DANGER_SIGN_LABELS_FR.get(item, item) for item in danger_signs]
        reason_suffix = ", ".join(labels) if labels else "signe de danger déclaré"
        referral = country_pack.referral_wording.get(
            "fr",
            "Référer vers la structure de santé appropriée selon le circuit local.",
        )
        possible_suspicions = tuple(primary_rule.result.get("possible_suspicions", []))
        return DecisionResult(
            urgency_level="urgent_referral",
            referral_required=True,
            immediate_action=ImmediateAction(
                category="urgent_referral",
                label="Référence urgente recommandée",
                text=referral,
            ),
            reason=f"Signes de danger de démonstration détectés : {reason_suffix}.",
            danger_signs_detected=tuple(danger_signs),
            possible_suspicions=possible_suspicions,
            missing_critical_data=tuple(missing_critical_data),
            actions_to_avoid=self._actions_to_avoid(),
            short_message=(
                "DEMO URGENCE: signes de danger. Référence urgente recommandée. "
                "Non validé pour soins réels."
            ),
            explanation_for_worker=(
                "Ces signes de démonstration sont traités comme des signaux d'alerte. "
                "Le moteur recommande une référence urgente par sécurité."
            ),
            source=source,
            considered_rule_ids=tuple(considered_rule_ids),
            triggered_rule_ids=tuple(rule.rule_id for rule in triggered_rules),
            scope_role="",
            forbidden_content_removed=("diagnosis", "prescription", "dosage", "medication"),
        )

    def _cannot_determine_result(
        self,
        triggered_rules: Sequence[Rule],
        considered_rule_ids: Sequence[str],
        missing_critical_data: Sequence[str],
        source: SourceMetadata,
    ) -> DecisionResult:
        return DecisionResult(
            urgency_level="cannot_determine",
            referral_required=None,
            immediate_action=ImmediateAction(
                category="ask_missing_questions",
                label="Données critiques manquantes",
                text="Compléter les données critiques manquantes sans retarder une référence si l'état inquiète.",
            ),
            reason="Données critiques insuffisantes pour une classification de démonstration fiable.",
            danger_signs_detected=(),
            possible_suspicions=(
                "Information insuffisante — formulation de démonstration, pas un diagnostic.",
            ),
            missing_critical_data=tuple(missing_critical_data),
            actions_to_avoid=self._actions_to_avoid(),
            short_message="DEMO: données critiques manquantes. Ne pas utiliser pour soins réels.",
            explanation_for_worker=(
                "Le moteur ne peut pas classer cette situation de démonstration sans les données critiques."
            ),
            source=source,
            considered_rule_ids=tuple(considered_rule_ids),
            triggered_rule_ids=tuple(rule.rule_id for rule in triggered_rules),
            scope_role="",
            forbidden_content_removed=("diagnosis", "prescription", "dosage", "medication"),
        )

    def _routine_demo_result(
        self,
        triggered_rules: Sequence[Rule],
        considered_rule_ids: Sequence[str],
        source: SourceMetadata,
    ) -> DecisionResult:
        return DecisionResult(
            urgency_level="routine_guidance",
            referral_required=False,
            immediate_action=ImmediateAction(
                category="routine_guidance",
                label="Suivre les protocoles locaux",
                text=(
                    "Aucun signe de danger de démonstration n'a été détecté dans les données structurées. "
                    "Continuer selon les protocoles locaux et demander un avis si inquiétude."
                ),
            ),
            reason="Aucun signe de danger de démonstration détecté dans les champs fournis.",
            danger_signs_detected=(),
            possible_suspicions=(
                "Aucune suspicion clinique n'est produite par ce moteur de démonstration.",
            ),
            missing_critical_data=(),
            actions_to_avoid=self._actions_to_avoid(),
            short_message="DEMO: pas de signe de danger fourni. Suivre protocoles locaux. Non validé.",
            explanation_for_worker=(
                "Cette sortie ne rassure pas cliniquement; elle montre seulement qu'aucune règle de danger "
                "de démonstration n'a été déclenchée."
            ),
            source=source,
            considered_rule_ids=tuple(considered_rule_ids),
            triggered_rule_ids=tuple(rule.rule_id for rule in triggered_rules),
            scope_role="",
            forbidden_content_removed=("diagnosis", "prescription", "dosage", "medication"),
        )

    def _danger_signs_detected(self, payload: Mapping[str, Any]) -> tuple[str, ...]:
        clinical_inputs = payload.get("clinical_inputs", {})
        danger_signs = (
            clinical_inputs.get("danger_signs", {}) if isinstance(clinical_inputs, dict) else {}
        )
        if not isinstance(danger_signs, dict):
            return ()
        return tuple(key for key in sorted(danger_signs) if danger_signs.get(key) is True)

    def _actions_to_avoid(self) -> tuple[str, ...]:
        return (
            "Ne pas présenter cette sortie comme un diagnostic.",
            "Ne pas prescrire de médicament ou dosage à partir de cette démonstration.",
            "Ne pas retarder une référence urgente pour compléter des données non disponibles.",
        )
