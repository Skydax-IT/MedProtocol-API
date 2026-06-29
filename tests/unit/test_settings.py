from __future__ import annotations

import pytest

from app.config import Settings


def test_settings_support_online_demo_environment_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "demo")
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("DEMO_TENANT_ID", "tenant_demo_online")

    settings = Settings()

    assert settings.environment == "demo"
    assert settings.demo_mode is True
    assert settings.database_url == "sqlite+pysqlite:///:memory:"
    assert settings.demo_tenant_slug == "tenant_demo_online"
    assert settings.demo_label == "v0.1.0 hosted demo mode"


def test_settings_can_load_without_env_file() -> None:
    settings = Settings(_env_file=None)

    assert settings.environment in {"local", "demo", "production"}
    assert settings.database_url


def test_settings_normalize_neon_postgres_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://user:pass@example.neon.tech/db?sslmode=require",
    )

    settings = Settings()

    assert settings.database_url.startswith("postgresql+psycopg://")


def test_settings_accept_legacy_local_environment_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MEDPROTOCOL_ENVIRONMENT", "local-demo")

    settings = Settings()

    assert settings.environment == "local"


def test_settings_reject_wildcard_cors_in_production(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "*")

    settings = Settings()

    with pytest.raises(ValueError, match="Wildcard CORS"):
        _ = settings.cors_allowed_origin_list
