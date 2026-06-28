#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker was not found."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Stopping MedProtocol API demo containers..."
docker compose down
echo "Stopped."
