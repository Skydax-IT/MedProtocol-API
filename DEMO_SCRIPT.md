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

> MedProtocol API is an API-first, deterministic protocol engine for frontline health system integrations. This is not a medical chatbot and not a clinical product. It is a demo environment using fake, non-validated rules.

Point out:

- `DEMO ONLY — NOT FOR REAL PATIENT CARE`;
- no real patient data;
- no validated clinical protocol;
- links to Demo UI, API Docs, ReDoc, and Health.

## 3. Open the Demo UI

Click:

```text
Open Demo UI
```

Or open:

http://localhost:8000/demo

Say:

> These are predefined fake cases. I will not enter any real patient information.

## 4. First Case to Click

Click:

```text
Child with danger signs
```

Say:

> This fake case demonstrates danger-sign-first triage. The API classifies urgency before returning any action text.

## 5. Explain the Result

Point to:

- urgency level;
- referral required;
- immediate action;
- danger signs detected;
- missing critical data;
- short SMS/USSD message;
- protocol and rule metadata.

Say:

> The output includes the demo rule ID and protocol version so an integrator can audit why the response happened. It is not a diagnosis and does not include medication or dosage.

## 6. Show the Audit ID

Point to:

```text
Audit ID
```

Say:

> Every evaluation creates an audit record. This is important for traceability, governance, and later safety review.

Click:

```text
View audit record
```

Say:

> The audit record shows the normalized input, triggered rules, missing data, output shown, and protocol metadata.

## 7. Show API Docs

Open:

http://localhost:8000/docs

Say:

> This is API-first. A partner system such as a field app, SMS/USSD gateway, DHIS2/OpenMRS-like system, or NGO tool would call these endpoints.

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

