#!/usr/bin/env bash
set -euo pipefail

if [ "${DEMO_MODE:-}" != "true" ]; then
  echo "Refusing to initialize hosted demo data because DEMO_MODE is not true."
  echo "Set APP_ENV=demo and DEMO_MODE=true for the hosted demo environment."
  exit 1
fi

if [ "${APP_ENV:-}" = "production" ]; then
  echo "Refusing to seed demo data when APP_ENV=production."
  exit 1
fi

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding fake demo tenant, hashed demo API key, and demo-only rules..."
python -m app.seed

echo "Hosted demo database initialization complete."
