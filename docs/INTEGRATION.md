# Integration

MedProtocol API is headless and integration-first. Partner systems call REST endpoints with structured JSON.

## Authentication

Send an API key on every `/v1` request:

```http
X-API-Key: mp_test_demo_local_only_change_me
X-Request-ID: optional-client-request-id
X-Correlation-ID: optional-cross-system-correlation-id
```

The server stores only hashed API keys.

## Triage Evaluation

```bash
curl -sS -X POST http://localhost:8000/v1/triage/evaluate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mp_test_demo_local_only_change_me" \
  --data-binary "@examples/json/evaluate_child_danger.request.json"
```

The response includes urgency, referral flag, role-adapted action text, missing data, source protocol/rule metadata, and `audit_id`.

## SMS/USSD Flow

Use `POST /v1/triage/next-question` to ask one prioritized danger-sign question at a time. The engine removes already answered questions and sorts by priority.

## Future Interoperability

FHIR, DHIS2, OpenMRS, CommCare, and OpenSRP mappings are intentionally not implemented in this MVP. Candidate mappings include structured answers to `QuestionnaireResponse`, vitals to `Observation`, and audit/referral outputs to partner-specific events.
