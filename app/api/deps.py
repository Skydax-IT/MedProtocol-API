from __future__ import annotations

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session

from app.api.errors import forbidden, unauthorized
from app.infrastructure.database import get_db_session
from app.infrastructure.repositories.api_key_repository import APIKeyRepository, AuthenticatedTenant


def get_db() -> Generator[Session]:
    yield from get_db_session()


def get_authenticated_tenant(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> AuthenticatedTenant:
    if not x_api_key:
        raise unauthorized()
    tenant = APIKeyRepository().authenticate(db, x_api_key)
    if tenant is None:
        raise unauthorized()
    request.state.tenant_id = tenant.tenant_id
    request.state.api_key_id = tenant.api_key_id
    return tenant


def enforce_tenant_country_module(
    tenant: AuthenticatedTenant,
    *,
    country_code: str,
    module_code: str | None = None,
) -> None:
    if tenant.allowed_countries and country_code.upper() not in tenant.allowed_countries:
        raise forbidden(
            "COUNTRY_NOT_ENABLED", f"Country {country_code.upper()} is not enabled for tenant."
        )
    if module_code and tenant.allowed_modules and module_code not in tenant.allowed_modules:
        raise forbidden("MODULE_NOT_ENABLED", f"Module {module_code} is not enabled for tenant.")
