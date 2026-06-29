# Security

## Current MVP Controls

- API-key authentication for `/v1` endpoints.
- PBKDF2-HMAC-SHA256 hashed API-key storage.
- Optional provider-managed `API_KEY_PEPPER` can be mixed into API key hashes for hosted environments.
- Key-prefix lookup without storing plaintext keys.
- Tenant-country and tenant-module authorization.
- Tenant-scoped audit retrieval.
- Request IDs and correlation IDs in response headers and logs.
- Strict Pydantic schemas with `extra="forbid"`.
- Restricted CORS defaults.
- Security headers for content type, frame, and referrer policy.
- Minimal patient data model with pseudonymous `patient_ref` only.

## Logging

Structured JSON logs avoid raw API keys and direct patient identifiers. Do not add names, phone numbers, addresses, or national identifiers to logs.

## Production Roadmap

- OAuth2 client credentials or mTLS for institutional clients.
- Managed secret rotation.
- Redis/API-gateway rate limiting.
- SIEM export.
- WAF rules.
- SAST, DAST, dependency scanning, and SBOM generation.
- Penetration testing and threat modeling.
- Backup, restore, and audit-retention policies.
