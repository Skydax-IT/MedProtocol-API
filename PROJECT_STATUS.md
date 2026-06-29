# Project Status

## Current MVP Status

MedProtocol API is a local and online-demo-ready prototype of a deterministic, protocol-based triage API. It is designed to show architecture, integration patterns, auditability, versioned demo rules, role-based output adaptation, and offline bundle concepts.

This is not a medical product and is not ready for real clinical use.

Release checkpoint: `v0.1.0-local-demo` marks the local demo MVP checkpoint.

Current product step: `v0.4-polished-business-site` makes the public demo feel like a polished, high-trust product website before online sharing.

Version labels:

- API version: `0.1.0`
- Demo UX version: `0.4.0`
- Product stage: prototype
- Clinical status: demo only, not validated for real care

## Implemented

- FastAPI backend with OpenAPI docs.
- Docker Compose local environment with PostgreSQL and API containers.
- One-command demo scripts for start, stop, reset, and logs.
- Mac double-click command files for non-technical local use.
- Polished business/product overview at `http://localhost:8000`.
- Guided non-technical demo at `http://localhost:8000/guided-demo`.
- Technical Demo Console at `http://localhost:8000/demo`.
- Demo-only deterministic rule engine.
- Demo country packs for `CF` and `TD`.
- Demo scopes for community health worker, nurse, midwife, and doctor.
- API-key authentication with hashed key storage.
- Tenant-aware request handling.
- Audit trail persistence and tenant-scoped audit retrieval.
- Offline bundle manifest endpoint.
- Unit, integration, and golden tests.
- Docker-based test and lint commands.
- `/ready` readiness endpoint for hosted demo checks.
- Render/Neon deployment preparation docs.
- Business demo checklist for pre-sharing review.
- Structured `/version` fields for API version, demo UX version, product stage, and clinical status.

## Verified Locally

- Docker build/start works.
- `http://localhost:8000/health` returns OK.
- `http://localhost:8000` loads the business overview.
- `http://localhost:8000/guided-demo` loads the guided demo.
- `http://localhost:8000/demo` loads the Technical Demo Console.
- Fake demo cases return structured triage responses.
- Audit lookup works for generated audit IDs.
- `make test` passes in Docker.
- `make lint` passes in Docker.
- `make check` passes locally.

## Clinical Safety Status

All bundled rules are demo-only, draft, not validated for real care, and not for real patient care.

The demo does not provide:

- diagnosis;
- treatment recommendations;
- medication;
- dosage;
- prescription;
- medical procedure guidance;
- validated clinical protocol content.

No AI or LLM makes medical decisions.

## Known Limitations

- Demo API key is local-only and intentionally simple.
- In-memory rate limiting is not production-grade.
- Demo rules are artificial architecture examples.
- No clinical validation workflow exists yet.
- No production deployment pipeline exists yet; only hosted demo preparation docs exist.
- No formal privacy impact assessment has been completed.
- No real interoperability mapping has been implemented.

## Not Ready For

- Real patient care.
- Clinical pilot use.
- Government or NGO deployment.
- Production hosting.
- Real medical protocol execution.
- Storage of real patient data.
- Security review sign-off.

## Next Recommended Steps

1. Keep all demos fake-data-only.
2. Use `/` for the business overview and `/guided-demo` for non-technical review.
3. Use `/docs` and `/demo` only for technical review.
4. Collect feedback from NGO, clinical, ministry, and integrator stakeholders.
5. Define a clinical governance process before adding any real protocol content.
6. Add deployment and operational controls only after the architecture is reviewed.
