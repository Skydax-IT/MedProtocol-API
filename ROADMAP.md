# Roadmap

## Phase 0 — Local Technical Demo

Goal: show the architecture and integration concept using fake data only.

What to build:

- Docker-first local demo.
- Landing page and browser demo UI.
- Deterministic demo rule engine.
- Audit records.
- Demo API docs.

What not to build yet:

- Real clinical rules.
- Production hosting.
- Complex frontend dashboard.

Validation criteria:

- Non-technical founder can start and test locally.
- Fake demo cases work.
- Tests and lint pass in Docker.

## Phase 1 — API Hardening

Goal: make the API easier for technical partners to review.

What to build:

- Better API error examples.
- Request and response examples in OpenAPI.
- Stronger API-key management plan.
- Rate-limiting design.
- CI checks.

What not to build yet:

- Real patient workflows.
- Real clinical protocol content.

Validation criteria:

- Technical reviewer can run the project and understand the API contract.
- Security gaps are documented.

## Phase 2 — Medical Protocol Validation Workflow

Goal: define how real protocol content would be authored, reviewed, approved, and versioned.

What to build:

- Rule authoring process.
- Clinical review checklist.
- Version approval workflow.
- Change history and rollback process.

What not to build yet:

- Autonomous medical decision-making.
- AI-generated clinical rules.

Validation criteria:

- Clinical governance process is documented before any real protocol is added.

## Phase 3 — Partner/Integrator Feedback

Goal: test whether the API shape fits NGO, ministry, and digital health workflows.

What to build:

- Fake-data integration examples.
- Partner feedback questionnaire.
- Sample SMS/USSD flow.
- Example DHIS2/OpenMRS-like mapping notes.

What not to build yet:

- Live integration with real systems.
- Real patient data ingestion.

Validation criteria:

- Integrators understand how they would call the API.
- Feedback identifies missing fields or workflow needs.

## Phase 4 — Offline SDK/Bundles

Goal: make offline execution feasible for low-connectivity settings.

What to build:

- Signed bundle format.
- Integrity hashes.
- Offline evaluation package design.
- Offline audit sync concept.

What not to build yet:

- Unsigned clinical bundles.
- Unreviewed local rule updates.

Validation criteria:

- Same input plus same bundle version gives same output.
- Bundle provenance is clear.

## Phase 5 — Country Packs

Goal: support localized, validated configuration per country.

What to build:

- Country pack schema.
- Localization workflow.
- Country/module enablement.
- National validation metadata.

What not to build yet:

- Claims of ministry or WHO validation without evidence.

Validation criteria:

- Each country pack has clear source, approval, version, and expiry metadata.

## Phase 6 — Pilot Readiness

Goal: prepare for a tightly controlled, approved pilot.

What to build:

- Safety case.
- Privacy impact assessment.
- Monitoring plan.
- Incident response process.
- Partner training materials.
- Legal and governance approvals.

What not to build yet:

- Broad rollout.
- Unsupervised clinical use.

Validation criteria:

- Written approval from qualified clinical and governance stakeholders.
- Pilot scope and stop criteria are defined.

## Phase 7 — Production Readiness

Goal: meet operational, security, and governance standards for production use.

What to build:

- Production deployment architecture.
- Secrets management.
- Strong authentication.
- Observability and SIEM export.
- Backup and restore.
- Penetration testing.
- Formal support and incident processes.

What not to build yet:

- Expansion beyond validated protocols and approved geographies.

Validation criteria:

- Security, privacy, clinical safety, operational readiness, and partner acceptance reviews pass.

