# MedProtocol API v0.1 — Local Demo MVP

Release tag: `v0.1.0-local-demo`

Checkpoint purpose: preserve the local Docker demo MVP before v0.2 hosted-demo preparation begins.

## What Is Working

- Docker Compose starts PostgreSQL and the FastAPI API.
- A non-technical local start path exists through `./scripts/demo_start.sh` and `start_demo.command`.
- `http://localhost:8000` shows a local landing page.
- `http://localhost:8000/demo` shows a browser demo using fake cases only.
- `http://localhost:8000/health` returns API health.
- `http://localhost:8000/docs` shows Swagger/OpenAPI docs.
- Demo triage evaluation creates an audit record.
- Tests and lint run inside Docker.
- `make check` verifies local health, demo pages, docs, Docker, tests, and Git status.

## What The Demo Proves

- Deterministic rule evaluation.
- Danger signs are prioritized first.
- Urgency is classified before action wording.
- Outputs include protocol and rule metadata.
- Outputs adapt by user role/scope.
- Missing critical data can be identified.
- SMS/USSD-ready summaries can be produced.
- Evaluation audit records are persisted.
- Offline bundle concepts can be exposed through an API endpoint.

## What Is Explicitly Demo-Only

- All bundled rules are fake demo rules.
- All protocol metadata is draft and not validated for real care.
- Country packs for `CF` and `TD` are demo packs only.
- The demo API key is local-only.
- Browser cases are fake cases only.
- The project is not for real patient care.

## What Is Not Implemented Yet

- Real validated clinical protocols.
- Diagnosis logic.
- Medication, dosage, prescription, treatment, or procedure logic.
- Production authentication and key rotation.
- Production deployment and monitoring.
- Formal interoperability mappings.
- Offline SDK execution.
- Clinical governance workflow.

## What Has Been Verified

- Docker build/start.
- Database migrations.
- Demo seed data.
- Health endpoint.
- Landing page.
- Demo page.
- Fake triage evaluation.
- Audit lookup.
- Swagger docs.
- Docker-based tests.
- Docker-based lint.

## Known Limitations

- This is a local demo, not a production system.
- Demo API key handling is intentionally simple.
- Rules are illustrative and non-clinical.
- No real patient data should be entered.
- Security controls are not sufficient for real health data.
- Clinical validation process is not yet implemented.

## What Must Happen Before Any Real Pilot

- Clinician-authored protocol content.
- Formal clinical safety review.
- National or partner protocol validation where applicable.
- Privacy impact assessment.
- Security threat modeling.
- Production-grade authentication and monitoring.
- Incident response and audit-retention policies.
- Partner training and pilot governance.
- Written approval from qualified clinical and operational stakeholders.
