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

echo "Stopping containers and removing the local demo database volume..."
docker compose down -v --remove-orphans

echo "Restarting from a clean demo state..."
"$ROOT_DIR/scripts/demo_start.sh"
