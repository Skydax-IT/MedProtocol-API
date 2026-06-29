#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker was not found."
  echo "Please install and start Docker Desktop, then run this script again."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker Desktop is not running."
  echo "Open Docker Desktop and wait until it says it is running, then try again."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example for the local demo."
fi

echo "Building and starting MedProtocol API demo containers..."
docker compose up -d --build postgres api

echo "Running database migrations..."
docker compose exec -T api alembic upgrade head

echo "Seeding local demo tenant, demo API key, protocols, and rules..."
docker compose exec -T api python -m app.seed

echo "Waiting for the API to respond..."
for attempt in $(seq 1 30); do
  if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
    break
  fi
  if [ "$attempt" -eq 30 ]; then
    echo "The API did not become ready in time."
    echo "Run ./scripts/demo_logs.sh to see what happened."
    exit 1
  fi
  sleep 2
done

cat <<'EOF'

MedProtocol API local demo is ready.

Open these URLs:
  Landing page: http://localhost:8000
  Guided demo:  http://localhost:8000/guided-demo
  Health check: http://localhost:8000/health
  Readiness:    http://localhost:8000/ready
  Technical demo console: http://localhost:8000/demo
  Swagger docs: http://localhost:8000/docs
  ReDoc docs:   http://localhost:8000/redoc

Local demo only. Do not enter real patient data.
EOF
