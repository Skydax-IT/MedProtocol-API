# Offline Bundles

`GET /v1/offline/bundles/{country_code}/{module_code}` returns a manifest-style demo bundle.

The MVP bundle includes:

- country code;
- module code;
- protocol versions;
- demo rules;
- questions;
- scopes;
- demo signature placeholder;
- expiry timestamp.

## Determinism

Future offline SDK execution must guarantee:

```text
same input + same bundle version = same output
```

Offline clients should sync audit records back to the server when connectivity returns.

## Future Work

- Signed bundle artifacts.
- Integrity hashes per file.
- Translation packs.
- Version pinning and expiry enforcement.
- Offline audit queue and replay protection.

