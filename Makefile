.PHONY: demo stop reset logs test lint typecheck check

.env:
	cp .env.example .env

demo:
	./scripts/demo_start.sh

stop:
	./scripts/demo_stop.sh

reset:
	./scripts/demo_reset.sh

logs:
	./scripts/demo_logs.sh

check: .env
	./scripts/project_check.sh

test: .env
	docker compose build api
	docker compose run --rm --no-deps api pytest

lint: .env
	docker compose build api
	docker compose run --rm --no-deps api ruff check .
	docker compose run --rm --no-deps api ruff format --check .

typecheck: .env
	docker compose build api
	docker compose run --rm --no-deps api mypy app
