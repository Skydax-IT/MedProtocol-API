from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from app.domain.enums import PregnancyStatus, Sex, UserRole
from app.schemas.common import (
    ImmediateActionResponse,
    ResponseMeta,
    SourceMetadataResponse,
    StrictBaseModel,
)


class PatientContext(StrictBaseModel):
    patient_ref: str | None = Field(default=None, max_length=128)
    age_months: int | None = Field(default=None, ge=0, le=1500)
    sex: Sex = Sex.unknown
    pregnancy_status: PregnancyStatus = PregnancyStatus.unknown
    weight_kg: float | None = Field(default=None, ge=0, le=300)


class EncounterContext(StrictBaseModel):
    country_code: str = Field(min_length=2, max_length=2)
    region_code: str | None = Field(default=None, max_length=32)
    setting: str | None = Field(default=None, max_length=80)
    user_role: UserRole
    connectivity: str | None = Field(default=None, max_length=40)
    language: str = Field(default="fr", min_length=2, max_length=8)


class DangerSigns(StrictBaseModel):
    convulsions: bool | None = None
    lethargy_or_unconscious: bool | None = None
    unable_to_drink_or_breastfeed: bool | None = None
    respiratory_distress: bool | None = None
    severe_bleeding: bool | None = None
    severe_abdominal_pain: bool | None = None
    severe_headache_or_visual_disturbance: bool | None = None


class Vitals(StrictBaseModel):
    temperature_c: float | None = Field(default=None, ge=25, le=45)
    respiratory_rate: int | None = Field(default=None, ge=0, le=120)
    heart_rate: int | None = Field(default=None, ge=0, le=260)


class ClinicalInputs(StrictBaseModel):
    main_complaint: str | None = Field(default=None, max_length=80)
    duration_days: int | None = Field(default=None, ge=0, le=365)
    danger_signs: DangerSigns = Field(default_factory=DangerSigns)
    vitals: Vitals = Field(default_factory=Vitals)


class ResourcesAvailable(StrictBaseModel):
    referral_transport_available: bool | None = None
    phone_network_available: bool | None = None
    rapid_malaria_test_available: bool | None = None
    ors_available: bool | None = None


class ClientContext(StrictBaseModel):
    external_encounter_id: str | None = Field(default=None, max_length=160)
    channel: str | None = Field(default=None, max_length=40)
    client_timestamp: datetime | None = None


class TriageEvaluateRequest(StrictBaseModel):
    patient_context: PatientContext
    encounter_context: EncounterContext
    clinical_inputs: ClinicalInputs
    resources_available: ResourcesAvailable = Field(default_factory=ResourcesAvailable)
    client_context: ClientContext = Field(default_factory=ClientContext)


class TriageEvaluateResponse(StrictBaseModel):
    audit_id: str
    urgency_level: str
    referral_required: bool | None
    immediate_action: ImmediateActionResponse
    reason: str
    danger_signs_detected: list[str]
    possible_suspicions: list[str]
    missing_critical_data: list[str]
    actions_to_avoid: list[str]
    short_message: str
    explanation_for_worker: str
    source: SourceMetadataResponse
    meta: ResponseMeta


class NextQuestionPatientContext(StrictBaseModel):
    age_months: int | None = Field(default=None, ge=0, le=1500)
    sex: Sex = Sex.unknown
    pregnancy_status: PregnancyStatus = PregnancyStatus.unknown


class NextQuestionEncounterContext(StrictBaseModel):
    country_code: str = Field(min_length=2, max_length=2)
    user_role: UserRole
    language: str = Field(default="fr", min_length=2, max_length=8)
    channel: str | None = Field(default=None, max_length=40)


class NextQuestionRequest(StrictBaseModel):
    session_id: str = Field(min_length=1, max_length=120)
    patient_context: NextQuestionPatientContext
    encounter_context: NextQuestionEncounterContext
    known_answers: dict[str, Any] = Field(default_factory=dict)


class NextQuestionResponseItem(StrictBaseModel):
    question_id: str
    text: str
    answer_type: str
    priority: int
    reason: str
    clinical_use_status: str = "not_for_real_patient_care"


class NextQuestionResponse(StrictBaseModel):
    session_id: str
    next_question: NextQuestionResponseItem | None
    can_evaluate_now: bool
    missing_critical_data: list[str]
    meta: ResponseMeta
