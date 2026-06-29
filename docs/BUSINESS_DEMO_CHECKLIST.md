# Business Demo Checklist

Use this before sharing the local or online demo with non-technical reviewers.

## Public Overview

- [ ] The warning banner is visible on `/`.
- [ ] The homepage explains the product in under 60 seconds.
- [ ] The positioning is clear: `A protocol-based triage layer for frontline health systems`.
- [ ] The page does not require understanding Swagger, endpoints, JSON, or API keys.
- [ ] The integration story is clear.
- [ ] The page does not claim medical validation.
- [ ] The page does not claim real clinical readiness.

## Guided Demo

- [ ] `/guided-demo` loads.
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
