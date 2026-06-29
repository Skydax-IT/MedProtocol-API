# Testing Checklist

All checks use fake demo data only. Do not enter real patient data.

## Docker Startup Test

Command:

```bash
./scripts/demo_start.sh
```

Expected:

- Docker containers start successfully.
- Migrations run successfully.
- Demo data is seeded.
- The script prints `MedProtocol API local demo is ready.`

## Health Endpoint Test

Open:

http://localhost:8000/health

Expected:

```json
{
  "status": "ok",
  "service": "medprotocol-api"
}
```

The timestamp value will vary.

## Readiness Endpoint Test

Open:

http://localhost:8000/ready

Expected:

```json
{
  "status": "ready",
  "service": "medprotocol-api",
  "environment": "local",
  "checks": {
    "api": "ok",
    "database": "ok",
    "demo_rules": "ok"
  }
}
```

## Public Website and Guided Demo Test

Open the landing page:

http://localhost:8000

Expected:

- Product name says `MedProtocol API`.
- Warning banner says `Demo only — not for real patient care`.
- The positioning says `A protocol-based triage layer for frontline health systems`.
- The primary button says `Try the guided demo`.
- The page explains the field problem, polished integration flow, safety posture, and prototype version labels.

Open:

http://localhost:8000/guided-demo

Expected:

- Banner says `Demo only — not for real patient care`.
- Fake case cards are visible.
- Clicking `Child with danger signs` and `Run demo triage` shows `urgent_referral`.
- An audit ID beginning with `aud_` appears.
- Technical JSON is hidden by default under developer details.

Technical reviewers can also open:

http://localhost:8000/demo

Expected:

- Page title says `Technical Demo Console`.
- JSON and audit inspection tools are available.

## Swagger Docs Test

Open:

http://localhost:8000/docs

Expected:

- Swagger UI loads.
- Endpoints under `/v1` are visible.

## Evaluate Endpoint Test

Command:

```bash
curl -sS -X POST http://localhost:8000/v1/triage/evaluate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mp_test_demo_local_only_change_me" \
  --data-binary "@examples/json/evaluate_child_danger.request.json"
```

Expected:

- `urgency_level` is `urgent_referral`.
- `referral_required` is `true`.
- `source.rule_ids` includes `demo_child_danger_001`.
- `clinical_use_status` is `not_for_real_patient_care`.
- `real_care_validation_status` is `not_validated_for_real_care`.

## Next-Question Endpoint Test

Command:

```bash
examples/curl/next_question_child.sh
```

Expected:

- `next_question.question_id` is `child_danger_lethargy`.
- `can_evaluate_now` is `false`.
- `clinical_use_status` is `not_for_real_patient_care`.

## Audit Endpoint Test

Steps:

1. Run the evaluate endpoint test.
2. Copy the returned `audit_id`.
3. Open:

```text
http://localhost:8000/v1/audit/YOUR_AUDIT_ID
```

The browser will not include the API key, so use curl:

```bash
curl -sS http://localhost:8000/v1/audit/YOUR_AUDIT_ID \
  -H "X-API-Key: mp_test_demo_local_only_change_me"
```

Expected:

- The same `audit_id` is returned.
- `triggered_rules` includes `demo_child_danger_001`.
- No raw API key is returned.

## Offline Bundle Endpoint Test

Command:

```bash
curl -sS http://localhost:8000/v1/offline/bundles/CF/child_triage \
  -H "X-API-Key: mp_test_demo_local_only_change_me"
```

Expected:

- `bundle_id` is `CF-child_triage-DEMO_DRAFT_NOT_VALIDATED`.
- `signature` is `demo-signature-placeholder`.
- Rules are marked demo-only and not for real patient care.

## Pytest Command

Run tests inside Docker:

```bash
make test
```

Expected:

- Pytest runs inside the Python 3.13 API container.
- All tests pass.

## Lint Command

Run lint inside Docker:

```bash
make lint
```

Expected:

- Ruff check passes.
- Ruff format check passes.

## Version Endpoint Test

Open:

http://localhost:8000/version

Expected:

- `api_version` is `0.1.0`.
- `demo_version` is `0.4.0`.
- `product_stage` is `prototype`.
- `clinical_status` is `demo_only_not_validated`.

## Reset Test

Command:

```bash
./scripts/demo_reset.sh
```

Expected:

- Containers stop.
- Local demo database volume is removed.
- Containers restart.
- Migrations and seed data run again.
- Business overview works at http://localhost:8000.
- Guided demo works at http://localhost:8000/guided-demo.
