# Business Demo Checklist

Use this before sharing the local or online demo with non-technical reviewers.

## Public Overview

- [ ] The warning banner is visible on `/`.
- [ ] The homepage feels polished, modern, and credible for non-technical stakeholders.
- [ ] The homepage explains the product in under 30-60 seconds.
- [ ] The positioning is clear: `A protocol-based triage layer for frontline health systems`.
- [ ] The page does not require understanding Swagger, endpoints, JSON, or API keys.
- [ ] The hero shows a clean field observation → API engine → triage output visual flow.
- [ ] The integration story is clear.
- [ ] API version and demo UX version are separated clearly.
- [ ] The page does not claim medical validation.
- [ ] The page does not claim real clinical readiness.

## Guided Demo

- [ ] `/guided-demo` loads.
- [ ] It feels like a product walkthrough, not a developer tool.
- [ ] Fake cases are clearly marked as demonstration only.
- [ ] The guided demo works without typing real information.
- [ ] JSON is hidden by default in a developer details section.
- [ ] Copy buttons work for the summary, SMS/USSD message, and technical JSON.
- [ ] The result explains urgency, referral flag, danger signs, missing data, and traceability.
- [ ] Safety language is visible.

## Technical Review Path

- [ ] `/demo` is labeled `Technical Demo Console`.
- [ ] `/docs` remains available for API/technical review.
- [ ] `/redoc` remains available as alternative API docs.
- [ ] `/health` and `/ready` work.

## Safety Review

- [ ] No real patient data is used.
- [ ] No real-care claims are made.
- [ ] No diagnosis claim appears.
- [ ] No treatment, medication, dosage, prescription, or procedure logic appears.
- [ ] All demo cases use fake data only.
- [ ] Screenshots are taken for overview, guided demo, result, safety banner, and technical docs.
