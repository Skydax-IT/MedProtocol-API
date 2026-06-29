# Roadmap

## Phase 0 — Local Technical Demo

Goal: show the architecture and integration concept using fake data only.

Status: completed as `v0.1.0-local-demo`.

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

## Phase 1 — Online Demo Preparation

Goal: make the fake-data demo shareable online for early feedback using free or low-cost hosted services.

Status: completed and merged from `v0.2-online-demo-prep`.

What to build:

- Render/Neon deployment preparation.
- Hosted demo environment settings.
- `/ready` readiness endpoint.
- Online demo verification checklist.
- Documentation for safe hosted demo initialization.

What not to build yet:

- Real patient workflows.
- Real clinical protocol content.
- Production security claims.
- Paid infrastructure requirements.

Validation criteria:

- Hosted demo can expose `/`, `/demo`, `/health`, `/ready`, `/docs`, and `/redoc`.
- Warning banners remain visible.
- Fake cases run and produce audit IDs.
- No real patient data is used.

## Phase 2 — Business Demo UX

Goal: make the fake-data demo understandable for NGO project managers, public health advisors, clinicians, ministries, funders, and non-technical decision makers.

Status: completed and merged from `v0.3-business-demo-ux`.

What to build:

- Business-oriented overview at `/`.
- Guided non-technical demo at `/guided-demo`.
- Technical Demo Console preserved at `/demo`.
- Technical docs preserved at `/docs` and `/redoc`.
- Business demo checklist before sharing.

What not to build yet:

- Product dashboard.
- Real patient workflows.
- Real clinical protocol content.
- Claims of medical validation.

Validation criteria:

- Non-technical reviewer can understand the homepage in under 60 seconds.
- Guided demo works without Swagger, JSON, API keys, or endpoint knowledge.
- Safety warnings remain visible.
- Technical review path remains available.

## Phase 3 — Polished Public Demo Site

Goal: make the public demo feel like a modern, high-trust health-tech/public-sector SaaS website while keeping the backend simple and safe.

Status: underway on `v0.4-polished-business-site`.

What to build:

- Polished homepage visual design.
- Animated non-JSON hero flow.
- Refined guided demo walkthrough.
- Clear version separation between API version and demo UX version.
- Navigation that leads with overview, guided demo, integration, safety, and technical docs.

What not to build yet:

- Heavy frontend framework.
- Real clinical workflows.
- Real protocol content.
- Production-readiness claims.

Validation criteria:

- Homepage feels credible for NGO, ministry, clinical, funder, and integrator review.
- Warnings remain visible.
- Guided demo remains fake-data-only.
- Tests, lint, and project checks pass.

## Phase 4 — API Hardening

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

## Phase 5 — Medical Protocol Validation Workflow

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

## Phase 6 — Partner/Integrator Feedback

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

## Phase 7 — Offline SDK/Bundles

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

## Phase 8 — Country Packs

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

## Phase 9 — Pilot Readiness

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

## Phase 10 — Production Readiness

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
