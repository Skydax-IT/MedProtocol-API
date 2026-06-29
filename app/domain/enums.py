from __future__ import annotations

from enum import StrEnum


class ClinicalUseStatus(StrEnum):
    not_for_real_patient_care = "not_for_real_patient_care"


class ValidationStatus(StrEnum):
    demo_only = "demo_only"


class ProtocolStatus(StrEnum):
    draft = "draft"


class UrgencyLevel(StrEnum):
    emergency = "emergency"
    urgent_referral = "urgent_referral"
    same_day_assessment = "same_day_assessment"
    routine_guidance = "routine_guidance"
    self_care_or_monitoring = "self_care_or_monitoring"
    cannot_determine = "cannot_determine"


class Sex(StrEnum):
    female = "female"
    male = "male"
    unknown = "unknown"


class PregnancyStatus(StrEnum):
    pregnant = "pregnant"
    not_pregnant = "not_pregnant"
    not_applicable = "not_applicable"
    unknown = "unknown"


class UserRole(StrEnum):
    community_health_worker = "community_health_worker"
    nurse = "nurse"
    midwife = "midwife"
    doctor = "doctor"
