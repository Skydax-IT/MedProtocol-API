# Security and Privacy Notes

## Demo Scope

This project is currently a local demo. It must only be used with fake data.

Do not enter:

- patient names;
- phone numbers;
- addresses;
- national IDs;
- real encounter notes;
- any other real patient information.

## Demo API Keys

The bundled demo API key is local-demo only. It is not a production secret.

The application stores API keys hashed in the database, but the local demo key exists to make the browser demo easy to run. A production deployment would need managed secrets, key rotation, stronger authentication, monitoring, and operational controls.

For hosted demo environments, generate a new `DEMO_API_KEY` and `API_KEY_PEPPER` in the hosting provider dashboard. Do not commit those values to GitHub.

## Personal Data Minimization

The API is designed to avoid direct patient identifiers by default. Demo request schemas allow only a pseudonymous `patient_ref`, and the browser demo sends fake data only.

For real deployments, data minimization must be reviewed with privacy, legal, clinical, and implementation stakeholders.

## Audit Trail Purpose

Audit records exist to support traceability:

- which tenant called the API;
- what structured inputs were evaluated;
- which rule IDs triggered;
- what output was shown;
- which protocol version was used;
- what data was missing.

Audit trails are not a substitute for clinical validation or governance.

## Future Requirements Before Real Deployment

Before handling real health data, the project would need:

- privacy impact assessment;
- threat modeling;
- production-grade authentication;
- encryption and secret management review;
- access control review;
- audit retention policy;
- monitoring and incident response;
- backup and restore procedures;
- clinical safety governance;
- legal and regulatory review.

## Why Health Data Requires Stronger Controls

Medical and health data can cause harm if exposed, misused, misunderstood, or processed incorrectly. Even simple triage metadata can be sensitive. Production systems must be designed for confidentiality, integrity, availability, traceability, and clinical accountability.

## Why Free-Tier or Local Demo Use Is Not Suitable for Real Clinical Care

Local demos and free-tier hosting typically do not provide the governance, support, monitoring, security, privacy, uptime, and incident-response controls required for real clinical use. This project should remain fake-data-only until a formal pilot readiness process is completed.
