# Data Model

Core tables:

- `tenants`: client organization, status, allowed countries, allowed modules.
- `api_keys`: hashed tenant API keys, prefix lookup, status, expiry, revocation.
- `protocols`: protocol metadata and validation status.
- `protocol_versions`: version records with metadata.
- `rules`: deterministic rule definitions and safety flags.
- `audit_events`: per-evaluation audit trail.
- `offline_bundles`: future manifest persistence.

Audit events store normalized structured inputs, triggered rules, missing data, protocol metadata, and output shown. The schema avoids direct identifiers by default and allows only pseudonymous external references.

