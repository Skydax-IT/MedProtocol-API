# Deterministic Triage API

A deterministic, API-first protocol engine built to explore **auditable rule evaluation, tenant-aware access and structured decision workflows**.

Built with **FastAPI, PostgreSQL, SQLAlchemy and Pydantic**, the project focuses on explicit rules and traceable outputs rather than generative decision-making.

> **Important:** this repository is an experimental software prototype.  
> It is **not validated for real patient care**, does not provide medical diagnosis, and must not be used for clinical decision-making.

## Overview

Deterministic Triage API explores how structured protocol rules can be exposed through a modern backend API.

Instead of relying on generative models for decisions, the engine evaluates explicit deterministic rules and returns structured results that can be inspected and audited.

The prototype demonstrates:

- Deterministic protocol evaluation
- Structured API-driven workflows
- Role-aware output
- Tenant isolation
- API-key authentication
- Audit trails
- Versioned protocol definitions
- Offline bundle concepts
- Input and output validation
- Containerized local development

## Architecture

```text
Client
  │
  │ X-API-Key
  ▼
FastAPI
  │
  ├── Authentication / tenant scope
  ├── Pydantic validation
  │
  ▼
Protocol Engine
  │
  ├── Explicit YAML rules
  ├── Deterministic evaluation
  └── Role-aware output
  │
  ▼
Audit Layer
  │
  ▼
PostgreSQL
```

The decision engine evaluates explicit protocol definitions rather than generating dynamic clinical responses.

This makes the evaluation path easier to inspect, reproduce and audit.

## Core Capabilities

- Protocol discovery
- Deterministic rule evaluation
- Progressive question workflows
- Tenant-aware API access
- Country and module scoping
- Audit record retrieval
- Version and capability endpoints
- Offline protocol bundle generation
- Request and correlation IDs
- Structured error handling

## API Endpoints

The prototype exposes endpoints including:

```text
GET  /health
GET  /ready
GET  /version

GET  /v1/capabilities
GET  /v1/protocols
GET  /v1/protocols/{protocol_id}

POST /v1/triage/evaluate
POST /v1/triage/next-question

GET  /v1/audit/{audit_id}
GET  /v1/offline/bundles/{country_code}/{module_code}
```

All `/v1` endpoints require an API key through:

```text
X-API-Key
```

Clients may optionally provide:

```text
X-Request-ID
X-Correlation-ID
```

## Tech Stack

### Backend

- **Python 3.13**
- **FastAPI**
- **Pydantic v2**
- **SQLAlchemy 2**
- **Alembic**
- **PostgreSQL**
- **PyYAML**

### Development & Quality

- **Docker**
- **Docker Compose**
- **uv**
- **Pytest**
- **pytest-cov**
- **Ruff**
- **mypy** with strict type checking

## Project Structure

```text
.
├── app/                    # Application and API logic
├── migrations/             # Alembic database migrations
├── protocols/              # Demo protocol definitions
├── tests/                  # Automated tests
├── examples/               # Example API requests
├── docs/                   # Technical documentation
├── scripts/                # Local demo utilities
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Getting Started

### Requirements

- Python 3.13+
- Docker
- Docker Compose
- `uv`

### Setup

Clone the repository:

```bash
git clone https://github.com/Skydax-IT/deterministic-triage-api.git
cd deterministic-triage-api
```

Create the environment file:

```bash
cp .env.example .env
```

Install dependencies:

```bash
uv sync
```

Start PostgreSQL:

```bash
docker compose up -d
```

Run database migrations:

```bash
uv run alembic upgrade head
```

Seed the demo database:

```bash
uv run python -m app.seed
```

Start the API:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## API Documentation

FastAPI automatically exposes interactive API documentation:

```text
Swagger UI
http://localhost:8000/docs

ReDoc
http://localhost:8000/redoc
```

## Example Request

An example deterministic evaluation can be executed with:

```bash
examples/curl/evaluate_child_danger.sh
```

Or directly with `curl`:

```bash
curl -sS -X POST http://localhost:8000/v1/triage/evaluate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mp_test_demo_local_only_change_me" \
  --data-binary "@examples/json/evaluate_child_danger.request.json"
```

The bundled API key is intended for local demonstration only and should never be reused in a shared environment.

## Testing & Code Quality

Run the test suite:

```bash
make test
```

Run linting:

```bash
make lint
```

Run all checks:

```bash
make check
```

Run strict static type checking:

```bash
uv run mypy app
```

## Security & Reliability

The prototype includes several backend security and reliability patterns:

- API keys stored as cryptographic hashes
- Tenant-aware authorization
- Country and module access scoping
- Tenant-scoped audit retrieval
- Pydantic input validation
- Unexpected fields rejected by default
- Request and correlation IDs
- Restricted CORS configuration
- Structured application logging
- Basic API rate limiting

The bundled in-memory rate limiter is intended as a prototype guardrail and would need to be replaced by a distributed solution such as an API gateway or Redis-backed limiter for a production environment.

## Safety Boundaries

This repository intentionally separates **software architecture experimentation** from real clinical usage.

The bundled protocol rules are demonstration content and are explicitly marked as not validated for real care.

The system:

- Does not provide definitive diagnosis
- Does not prescribe medication or dosage
- Does not generate clinical decisions using an LLM
- Does not replace validated medical protocols
- Must not be used for real patient care

Any real-world clinical deployment would require validated protocols, clinical safety review, governance approval, privacy and security assessments, localization validation and operational monitoring.

## Project Status

This repository is an **archived experimental prototype** and is no longer under active development.

It is preserved as a technical demonstration of:

- FastAPI backend architecture
- Deterministic rule engines
- API authentication and tenant isolation
- Auditable decision workflows
- PostgreSQL persistence
- Runtime validation
- Automated testing
- Containerized development

## Disclaimer

This software is provided for **software engineering demonstration and research purposes only**.

It is not a medical device, diagnostic system or validated clinical decision-support tool.

## License

See the repository license for usage terms.