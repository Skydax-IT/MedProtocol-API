from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MEDPROTOCOL_",
        env_file=".env",
        extra="ignore",
    )

    service_name: str = "medprotocol-api"
    version: str = "0.1.0"
    commit: str = "local-dev"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://medprotocol:medprotocol@localhost:5432/medprotocol"
    cors_allowed_origins: str = ""
    log_level: str = "INFO"
    demo_api_key: str = "mp_test_demo_local_only_change_me"
    demo_tenant_slug: str = "tenant_demo"
    rate_limit_per_minute: int = 120

    @property
    def cors_allowed_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_allowed_origins.split(",") if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
