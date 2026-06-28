# Architecture

MedProtocol API follows a small hexagonal architecture.

```text
External systems
  -> FastAPI routes and schemas
  -> Application services
  -> Domain engine
  -> Infrastructure adapters
```

## Boundaries

- `app/api`: HTTP routes, dependencies, middleware, and error handlers.
- `app/schemas`: strict Pydantic request and response contracts.
- `app/application`: use cases such as triage evaluation, next question, audit retrieval, protocols, capabilities, and offline bundles.
- `app/domain`: deterministic framework-independent rule engine, missing-data detector, output composer, scope adapter, and safety guardrails.
- `app/infrastructure`: SQLAlchemy models, repositories, hashed API-key auth, and YAML rule loading.
- `app/data/demo`: demo-only protocols, rules, country packs, scopes, and questions.

The domain engine imports no FastAPI types, so it can later be packaged as an offline SDK.

## Evaluation Flow

1. Validate structured request with Pydantic.
2. Authenticate API key and resolve tenant.
3. Check tenant country/module access.
4. Load deterministic demo catalog.
5. Evaluate rules sorted by priority descending, then `rule_id`.
6. Prioritize urgent danger-sign rules.
7. Detect missing critical data.
8. Apply role/scope output constraints.
9. Compose JSON and SMS/USSD-friendly wording.
10. Persist tenant-scoped audit record.

No external API, LLM, random value, or free-text diagnosis is used during evaluation.

