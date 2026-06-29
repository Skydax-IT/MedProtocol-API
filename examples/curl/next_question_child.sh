#!/usr/bin/env sh
set -eu

API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
API_KEY="${MEDPROTOCOL_DEMO_API_KEY:-mp_test_demo_local_only_change_me}"

curl -sS -X POST "$API_BASE_URL/v1/triage/next-question" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -H "X-Request-ID: req_example_next_question" \
  -H "X-Correlation-ID: corr_example_next_question" \
  -d '{
    "session_id": "sess_demo_001",
    "patient_context": {
      "age_months": 24,
      "sex": "female",
      "pregnancy_status": "not_applicable"
    },
    "encounter_context": {
      "country_code": "CF",
      "user_role": "community_health_worker",
      "language": "fr",
      "channel": "ussd"
    },
    "known_answers": {
      "main_complaint": "fever",
      "duration_days": 2
    }
  }'
