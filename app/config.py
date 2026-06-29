from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    service_name: str = Field(
        default="medprotocol-api",
        validation_alias=AliasChoices("SERVICE_NAME", "MEDPROTOCOL_SERVICE_NAME"),
    )
    version: str = Field(
        default="0.1.0",
        validation_alias=AliasChoices("APP_VERSION", "MEDPROTOCOL_VERSION"),
    )
    commit: str = Field(
        default="local-dev",
        validation_alias=AliasChoices("APP_COMMIT", "MEDPROTOCOL_COMMIT", "RENDER_GIT_COMMIT"),
    )
    app_env: str = Field(
        default="local",
        validation_alias=AliasChoices("APP_ENV", "MEDPROTOCOL_ENVIRONMENT"),
    )
    database_url: str = Field(
        default="postgresql+psycopg://medprotocol:medprotocol@localhost:5432/medprotocol",
        validation_alias=AliasChoices("DATABASE_URL", "MEDPROTOCOL_DATABASE_URL"),
    )
    cors_allowed_origins: str = Field(
        default="",
        validation_alias=AliasChoices("CORS_ALLOWED_ORIGINS", "MEDPROTOCOL_CORS_ALLOWED_ORIGINS"),
    )
    log_level: str = Field(
        default="INFO",
        validation_alias=AliasChoices("LOG_LEVEL", "MEDPROTOCOL_LOG_LEVEL"),
    )
    demo_api_key: str = Field(
        default="mp_test_demo_local_only_change_me",
        validation_alias=AliasChoices("DEMO_API_KEY", "MEDPROTOCOL_DEMO_API_KEY"),
    )
    demo_tenant_id: str = Field(
        default="tenant_demo",
        validation_alias=AliasChoices("DEMO_TENANT_ID", "MEDPROTOCOL_DEMO_TENANT_SLUG"),
    )
    demo_mode: bool = Field(
        default=True,
        validation_alias=AliasChoices("DEMO_MODE", "MEDPROTOCOL_DEMO_MODE"),
    )
    api_key_pepper: str = Field(
        default="",
        validation_alias=AliasChoices("API_KEY_PEPPER", "MEDPROTOCOL_API_KEY_PEPPER"),
    )
    rate_limit_per_minute: int = Field(
        default=120,
        validation_alias=AliasChoices("RATE_LIMIT_PER_MINUTE", "MEDPROTOCOL_RATE_LIMIT_PER_MINUTE"),
    )

    @field_validator("app_env")
    @classmethod
    def normalize_app_env(cls, value: str) -> str:
        normalized = value.strip().lower()
        aliases = {
            "development": "local",
            "dev": "local",
            "local-demo": "local",
            "online-demo": "demo",
        }
        normalized = aliases.get(normalized, normalized)
        if normalized not in {"local", "demo", "production"}:
            msg = "APP_ENV must be one of: local, demo, production."
            raise ValueError(msg)
        return normalized

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg://", 1)
        return value

    @property
    def cors_allowed_origin_list(self) -> list[str]:
        configured = [item.strip() for item in self.cors_allowed_origins.split(",") if item.strip()]
        if "*" in configured and self.app_env == "production":
            msg = "Wildcard CORS is not allowed when APP_ENV=production."
            raise ValueError(msg)
        if configured:
            return configured
        if self.app_env == "local":
            return ["http://localhost:8000", "http://127.0.0.1:8000"]
        return []

    @property
    def environment(self) -> str:
        return self.app_env

    @property
    def demo_tenant_slug(self) -> str:
        return self.demo_tenant_id

    @property
    def demo_label(self) -> str:
        if self.app_env == "demo":
            return f"v{self.version} hosted demo mode"
        if self.app_env == "production":
            return f"v{self.version} production config - clinical use disabled"
        return f"v{self.version} local demo MVP"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
