#!/usr/bin/env sh
set -eu

API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
API_KEY="${MEDPROTOCOL_DEMO_API_KEY:-mp_test_demo_local_only_change_me}"

curl -sS -X POST "$API_BASE_URL/v1/triage/evaluate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -H "X-Request-ID: req_example_child" \
  -H "X-Correlation-ID: corr_example_child" \
  --data-binary "@examples/json/evaluate_child_danger.request.json"
