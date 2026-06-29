# Screenshot Guide

Take screenshots using fake data only. Do not enter real patient data.

## Business Overview Page

URL:

```text
http://localhost:8000
```

What it demonstrates:

- Business-oriented demo entry point.
- Product name and positioning.
- Demo-only safety banner.
- Field problem, MedProtocol approach, safety-by-design, and integration story.
- Clear path to `View guided demo`.

## Guided Demo Before Running a Case

URL:

```text
http://localhost:8000/guided-demo
```

What it demonstrates:

- Non-technical reviewers do not need Swagger, JSON, or API keys.
- Fake story cases are predefined.
- No real patient data entry is needed.
- Safety warnings remain visible.

## Guided Demo Result After Child Danger Signs Case

Action:

Click `Child with danger signs`, then click `Run demo triage`.

What it demonstrates:

- Deterministic urgent referral output from fake demo danger signs.
- Danger signs detected.
- Missing critical data.
- SMS/USSD-ready summary.
- Plain-language explanation of why the output was generated.
- Traceability fields without making the user read JSON.

## Technical Details Section

Action:

After running a guided case, expand `Technical details for developers`.

What it demonstrates:

- Every evaluation creates an audit trail.
- The API records triggered rules, missing data, normalized inputs, and output shown.
- JSON and audit records are available for technical review but hidden by default.

## Technical Demo Console

URL:

```text
http://localhost:8000/demo
```

What it demonstrates:

- Developers and technical reviewers can still inspect JSON, audit IDs, and raw responses.
- The technical console is not the main non-technical experience.

## Swagger Docs

URL:

```text
http://localhost:8000/docs
```

What it demonstrates:

- This is API-first.
- Technical partners can inspect endpoints and schemas.
- The product can integrate with external systems.

## Health Endpoint

URL:

```text
http://localhost:8000/health
```

What it demonstrates:

- The local API is running and reachable.
- Docker startup worked.

## Roadmap and Project Status

Files:

```text
PROJECT_STATUS.md
ROADMAP.md
MILESTONE_V0_1_LOCAL_DEMO.md
```

What they demonstrate:

- Clear current status.
- Clear limitations.
- Practical next steps.
- Safety-aware path before any real pilot.
