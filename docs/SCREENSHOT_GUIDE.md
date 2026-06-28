# Screenshot Guide

Take screenshots using fake data only. Do not enter real patient data.

## Landing Page

URL:

```text
http://localhost:8000
```

What it demonstrates:

- Professional local demo entry point.
- Product name and positioning.
- Demo-only safety banner.
- Links to demo UI, API docs, ReDoc, and health check.

## Demo UI Before Running a Case

URL:

```text
http://localhost:8000/demo
```

What it demonstrates:

- Fake cases are predefined.
- No real patient data entry is needed.
- Safety warnings remain visible.

## Demo Result After Child Danger Signs Case

Action:

Click `Child with danger signs`.

What it demonstrates:

- Deterministic urgent referral output from fake demo danger signs.
- Danger signs detected.
- Missing critical data.
- SMS/USSD-ready summary.
- Protocol/rule metadata.
- Audit ID.

## Audit JSON Section

Action:

After running a case, click `View audit record`.

What it demonstrates:

- Every evaluation creates an audit trail.
- The API records triggered rules, missing data, normalized inputs, and output shown.
- Auditability is part of the architecture.

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

