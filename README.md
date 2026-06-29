# MedProtocol API

## Quickstart for Non-Technical Local Demo

1. Open Docker Desktop and wait until it is running.
2. Run `./scripts/demo_start.sh` or double-click `start_demo.command`.
3. Open `http://localhost:8000`.
4. Click `Try the guided demo`.
5. Stop with `./scripts/demo_stop.sh` or double-click `stop_demo.command`.

Useful founder-facing docs:

- [README_NON_TECHNICAL.md](README_NON_TECHNICAL.md)
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [MILESTONE_V0_1_LOCAL_DEMO.md](MILESTONE_V0_1_LOCAL_DEMO.md)
- [FOUNDER_NEXT_STEPS.md](FOUNDER_NEXT_STEPS.md)
- [docs/BUSINESS_DEMO_CHECKLIST.md](docs/BUSINESS_DEMO_CHECKLIST.md)
- [docs/SCREENSHOT_GUIDE.md](docs/SCREENSHOT_GUIDE.md)
- [docs/ENVIRONMENT_VARIABLES.md](docs/ENVIRONMENT_VARIABLES.md)
- [docs/DEPLOYMENT_RENDER_NEON.md](docs/DEPLOYMENT_RENDER_NEON.md)
- [docs/ONLINE_DEMO_CHECKLIST.md](docs/ONLINE_DEMO_CHECKLIST.md)
- [ROADMAP.md](ROADMAP.md)
- [SECURITY_AND_PRIVACY_NOTES.md](SECURITY_AND_PRIVACY_NOTES.md)

MedProtocol API is a demo-only, API-first, deterministic triage protocol engine for integration experiments with field health systems. It is not a diagnosis engine, not a medical chatbot, and not validated for real patient care.

All bundled clinical rules are seed demo rules marked:

- `validation_status: demo_only`
- `clinical_use_status: not_for_real_patient_care`
- `real_care_validation_status: not_validated_for_real_care`
- `protocol_version: DEMO_DRAFT_NOT_VALIDATED`

The MVP demonstrates architecture, deterministic rule evaluation, role-based output adaptation, auditability, tenant-aware API access, a polished business demo experience, and future offline bundle patterns.

Version labels are intentionally separate:

- API version: `0.1.0`
- Demo UX version: `0.4.0`
- Product stage: `prototype`
- Clinical status: `demo_only_not_validated`

## Stack

- Python 3.13 target runtime
- FastAPI and Pydantic v2
- SQLAlchemy 2.0 and Alembic
- PostgreSQL 18 via Docker Compose
- Pytest, Ruff, mypy
- uv for dependency management

## Safety Boundaries

This repository must not be used for real clinical care. It does not provide definitive diagnosis, medication, dosage, prescription, or technical procedure logic. No LLM or generative AI is used for clinical decisions. The deterministic engine only evaluates explicit demo YAML rules.

## One-Command Local Demo

For a non-technical local demo on macOS, install Docker Desktop and run:

```bash
./scripts/demo_start.sh
```

Then open:

http://localhost:8000

For non-technical reviewers, open:

http://localhost:8000/guided-demo

More detailed non-technical instructions are in [README_NON_TECHNICAL.md](README_NON_TECHNICAL.md).

## Developer Setup

```bash
cp .env.example .env
uv sync
docker compose up -d
uv run alembic upgrade head
uv run python -m app.seed
uv run uvicorn app.main:app --reload
```

API docs:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Default local demo API key from `.env.example`:

```text
mp_test_demo_local_only_change_me
```

Change it before any shared environment. The key is stored hashed in the database by `python -m app.seed`.

## Required Endpoints

- `GET /health`
- `GET /ready`
- `GET /version`
- `GET /v1/capabilities`
- `GET /v1/protocols`
- `GET /v1/protocols/{protocol_id}`
- `POST /v1/triage/evaluate`
- `POST /v1/triage/next-question`
- `GET /v1/audit/{audit_id}`
- `GET /v1/offline/bundles/{country_code}/{module_code}`

All `/v1` endpoints require `X-API-Key`.
Clients may also send `X-Request-ID` and `X-Correlation-ID`; the API echoes both response headers.

## Example

```bash
examples/curl/evaluate_child_danger.sh
```

Or manually:

```bash
curl -sS -X POST http://localhost:8000/v1/triage/evaluate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mp_test_demo_local_only_change_me" \
  --data-binary "@examples/json/evaluate_child_danger.request.json"
```

## Tests and Checks

```bash
make test
make lint
make check
uv run mypy app
```

## Security Notes

- API keys are hashed with PBKDF2-HMAC-SHA256.
- Tenants are scoped by allowed countries and modules.
- Audit reads are tenant-scoped.
- Logs include request/tenant metadata but not raw API keys.
- Pydantic schemas forbid unexpected fields by default.
- CORS defaults to no allowed browser origins.
- The in-memory rate limiter is only an MVP guardrail; use an API gateway or Redis-backed limiter in production.

## Before Any Real Clinical Pilot

This prototype would need validated national protocols, clinical safety review, governance approval, localized content validation, threat modeling, privacy impact assessment, operational incident processes, integration testing with partner systems, and prospective monitoring. The current demo rules are not a substitute for that work.
