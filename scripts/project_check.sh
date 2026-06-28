#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0
WARN=0

section() {
  printf "\n== %s ==\n" "$1"
}

ok() {
  printf "OK: %s\n" "$1"
}

fail() {
  printf "FAIL: %s\n" "$1"
  WARN=1
}

section "Local Files"
if [ -f .env ]; then
  ok ".env exists"
else
  fail ".env is missing. Run ./scripts/demo_start.sh to create it from .env.example."
fi

section "Docker"
if command -v docker >/dev/null 2>&1; then
  ok "Docker command is installed"
  if docker info >/dev/null 2>&1; then
    ok "Docker Desktop is running"
  else
    fail "Docker Desktop is not running or not reachable"
  fi
else
  fail "Docker command not found"
fi

section "API Reachability"
if curl -fsS http://localhost:8000 >/dev/null 2>&1; then
  ok "API landing page is responding"
else
  fail "API landing page is not responding at http://localhost:8000"
fi

if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
  ok "/health is OK"
else
  fail "/health is not reachable"
fi

if curl -fsS http://localhost:8000/demo >/dev/null 2>&1; then
  ok "/demo is reachable"
else
  fail "/demo is not reachable"
fi

if curl -fsS http://localhost:8000/docs >/dev/null 2>&1; then
  ok "/docs is reachable"
else
  fail "/docs is not reachable"
fi

section "Tests"
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  if docker compose build api >/tmp/medprotocol_project_check_build.log 2>&1 \
    && docker compose run --rm --no-deps api pytest >/tmp/medprotocol_project_check_pytest.log 2>&1; then
    ok "Docker pytest passed"
  else
    fail "Docker build or pytest failed. See /tmp/medprotocol_project_check_build.log and /tmp/medprotocol_project_check_pytest.log"
  fi
else
  fail "Skipping tests because Docker is not available"
fi

section "Git"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short
else
  ok "Git is not initialized yet in this folder"
fi

section "Result"
if [ "$WARN" -eq 0 ]; then
  ok "Project check passed"
  exit "$PASS"
fi

fail "Project check completed with warnings or failures"
exit 1
