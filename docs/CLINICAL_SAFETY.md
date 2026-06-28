# Clinical Safety

This MVP is not clinically validated and is not for real patient care.

## Non-Negotiable Constraints

- No diagnosis is returned.
- No medication, dosage, prescription, or technical procedure logic is included.
- No LLM or generative AI makes clinical decisions.
- Every seed protocol and rule is marked `demo_only`, `draft`, `not_for_real_patient_care`, and `not_validated_for_real_care`.
- Danger signs are prioritized before any action wording.
- Urgency is classified before action text is composed.
- Missing critical data is reported.
- Source protocol metadata and rule IDs are returned in every decision.

## Demo Rule Scope

The bundled rules only demonstrate architecture:

- general insufficient-data handling;
- child 0-59 months demo danger signs;
- pregnancy demo danger signs;
- referral-oriented safety wording.

They are not WHO, ministry, or NGO-validated protocols.

## Needed Before Real Use

A real pilot would require clinician-authored protocols, national approval where applicable, independent safety review, versioned clinical governance, field validation, adverse-event monitoring, localization review, and formal deployment controls.
