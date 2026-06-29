# Environment Variables

This project reads settings from environment variables. For local testing, `scripts/demo_start.sh` creates `.env` from `.env.example` if `.env` is missing.

Never commit `.env`. It can contain real database URLs and API secrets. Generate online demo secrets inside Render, Neon, or the hosting provider dashboard.

## Variables

| Variable | What it does | Safe example | Required locally | Required online | Sensitive |
| --- | --- | --- | --- | --- | --- |
| `APP_ENV` | Tells the API which environment it is running in. Use `local`, `demo`, or `production`. | `local` | Yes | Yes | No |
| `DEMO_MODE` | Keeps the hosted demo in fake-data, demo-only mode. | `true` | Yes | Yes for online demo | No |
| `DATABASE_URL` | Database connection string used by SQLAlchemy and Alembic. | `postgresql+psycopg://user:password@host/dbname` | Yes | Yes | Yes |
| `API_KEY_PEPPER` | Extra secret mixed into API key hashes. Keep empty locally, generate a strong value online. | `generate-in-render-dashboard` | No | Yes | Yes |
| `DEMO_API_KEY` | API key used by the browser demo. The stored database value is hashed. | `generate-a-new-demo-key` | Yes | Yes | Yes |
| `DEMO_TENANT_ID` | Slug for the fake demo tenant. | `tenant_demo` | Yes | Yes | No |
| `CORS_ALLOWED_ORIGINS` | Comma-separated browser origins allowed to call the API from another website. | `https://your-render-app.onrender.com` | No | Usually yes | No |
| `LOG_LEVEL` | Logging detail. | `INFO` | No | No | No |
| `APP_VERSION` | Version shown by `/version`. | `0.1.0` | No | No | No |
| `APP_COMMIT` | Commit shown by `/version`. Render may set this automatically. | `local-dev` | No | No | No |
| `RATE_LIMIT_PER_MINUTE` | Simple MVP request limit per client. | `120` | No | No | No |

## Environment Modes

- `APP_ENV=local`: local Docker Desktop demo on your computer.
- `APP_ENV=demo`: hosted online demo for fake cases and feedback.
- `APP_ENV=production`: reserved for a future production setup. This prototype is not production-ready and must not be used for real patient care.

For the online demo use:

```text
APP_ENV=demo
DEMO_MODE=true
```

## Safety Notes

- Demo API keys are for local or hosted demo use only.
- Do not reuse the local key `mp_test_demo_local_only_change_me` online.
- Do not enter real patient data in local or online demo mode.
- Do not add real clinical protocols until a qualified clinical validation process exists.
