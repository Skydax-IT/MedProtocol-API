# Online Demo Checklist

Use this checklist only for a hosted fake-data demo. This is not a clinical pilot checklist.

## Before Deployment

- [ ] GitHub repository is pushed.
- [ ] `.env` is not committed.
- [ ] No real secrets are committed.
- [ ] No database volumes or local runtime files are committed.
- [ ] Demo rules are still marked `demo_only`, `draft`, `not_validated_for_real_care`, and `not_for_real_patient_care`.
- [ ] No real clinical protocols were added.
- [ ] No diagnosis, treatment, medication, dosage, prescription, or procedure logic was added.

## Render and Neon Setup

- [ ] Neon database created.
- [ ] Neon database connection string copied into Render only.
- [ ] Render web service created.
- [ ] GitHub repository connected to Render.
- [ ] Docker runtime selected.
- [ ] Environment variables configured.
- [ ] `APP_ENV=demo`.
- [ ] `DEMO_MODE=true`.
- [ ] New hosted-demo `DEMO_API_KEY` generated.
- [ ] `API_KEY_PEPPER` generated in Render.
- [ ] `.env` not uploaded or pasted into GitHub.

## Database Initialization

- [ ] Alembic migrations run.
- [ ] Demo seed command run.
- [ ] Only fake demo tenant/data seeded.
- [ ] No real patient data seeded.

## Public URL Verification

- [ ] `/health` returns OK.
- [ ] `/ready` returns ready.
- [ ] `/` loads as the polished business/product overview.
- [ ] `/` is understandable without Swagger or JSON knowledge.
- [ ] `/` shows API version `0.1.0` separately from demo UX version `0.4.0`.
- [ ] `/guided-demo` loads for non-technical reviewers.
- [ ] `/guided-demo` feels like a guided product walkthrough.
- [ ] `/demo` loads as the Technical Demo Console.
- [ ] `/docs` loads for API/technical review only.
- [ ] `/redoc` loads.
- [ ] Warning banner is visible.
- [ ] Text says `Demo only — not for real patient care`.
- [ ] Text says no real patient data.
- [ ] Guided fake case runs.
- [ ] Audit ID is generated.
- [ ] Raw JSON is hidden by default under technical details.
- [ ] Technical docs remain accessible but are not the main user experience.

## Safety Review

- [ ] No real patient data used during testing.
- [ ] No claim of clinical validation made.
- [ ] No claim that the tool diagnoses patients.
- [ ] No claim that the tool recommends treatment.
- [ ] Free-tier limitations understood.
