# Demo Script

## 1. Start the Demo

Say:

> This demo runs locally with Docker. It does not require installing Python or PostgreSQL manually.

Run:

```bash
./scripts/demo_start.sh
```

Or double-click:

```text
start_demo.command
```

## 2. Open the Landing Page

Open:

http://localhost:8000

Say:

> MedProtocol API is a protocol-based triage layer for frontline health systems. This polished demo shows how existing field tools could call deterministic protocol logic and receive traceable triage outputs.

Point out:

- `Demo only — not for real patient care`;
- no real patient data;
- no validated clinical protocol;
- no diagnosis or treatment recommendation;
- the `Try the guided demo` button;
- the integration story showing field tools, MedProtocol API, triage output, and audit trail.
- the version labels: API version `0.1.0`, demo UX version `0.4.0`, product stage `Prototype`, clinical status `Demo only`.

## 3. Open the Guided Demo

Click:

```text
Try the guided demo
```

Or open:

http://localhost:8000/guided-demo

Say:

> This page is for non-technical reviewers. It shows what a field app might send, what the API does, what comes back, and why the result is traceable.

## 4. First Case to Click

Click:

```text
Child with danger signs
```

Then click:

```text
Run demo triage
```

Say:

> This fake case demonstrates danger-sign-first triage. The API classifies urgency before returning any action text. It is not making a diagnosis.

## 5. Explain the Result

Point to:

- urgency level;
- referral required;
- immediate action;
- danger signs detected;
- missing critical data;
- short SMS/USSD message;
- why the output was generated.

Say:

> The result is written in simple language first. Technical details are hidden by default so non-technical reviewers do not need to understand JSON or Swagger.

## 6. Show Traceability

Point to:

```text
Step 3 — Traceability
```

Say:

> Every evaluation creates an audit record and includes the demo rule ID, protocol version, validation status, user role, and demo-only status. This is important for traceability, governance, and later safety review.

Click:

```text
Technical details for developers
```

Say:

> Developers can inspect the raw JSON response, audit record, and endpoint used, but this is not required for the business demo.

## 7. Optional Technical Review

Open:

http://localhost:8000/demo

Say:

> This is the Technical Demo Console for developers and technical reviewers who want JSON, audit IDs, and API testing.

Then open:

http://localhost:8000/docs

Say:

> Swagger is the technical API documentation. A partner system such as a field app, SMS/USSD gateway, DHIS2/OpenMRS-like system, or NGO tool would call these endpoints, but non-technical reviewers do not need to use this page.

## 8. Explain What It Is Not

Say:

> This is not a consumer medical chatbot. It does not use AI to make medical decisions. It does not diagnose, prescribe, or recommend treatment. Real clinical content would require expert protocol authoring, national validation, governance, safety review, and pilot approval.

## 9. Explain Future Integration Vision

Say:

> The long-term vision is to provide a protocol layer between data collection systems and safe, auditable triage outputs. The API can later support validated country packs, offline bundles, SMS/USSD workflows, and integration with existing health information systems.

## 10. Stop the Demo

Run:

```bash
./scripts/demo_stop.sh
```

Or double-click:

```text
stop_demo.command
```
