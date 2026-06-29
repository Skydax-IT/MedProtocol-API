from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.models import APIKeyModel, TenantModel
from app.infrastructure.security.hashing import api_key_prefix, verify_api_key


@dataclass(frozen=True)
class AuthenticatedTenant:
    tenant_id: str
    tenant_slug: str
    tenant_name: str
    api_key_id: str
    allowed_countries: tuple[str, ...]
    allowed_modules: tuple[str, ...]


class APIKeyRepository:
    def authenticate(self, session: Session, raw_key: str) -> AuthenticatedTenant | None:
        settings = get_settings()
        prefix = api_key_prefix(raw_key)
        key = (
            session.execute(
                select(APIKeyModel).where(
                    APIKeyModel.key_prefix == prefix, APIKeyModel.status == "active"
                )
            )
            .scalars()
            .first()
        )
        if key is None or key.revoked_at is not None:
            return None
        now = datetime.now(UTC)
        if key.expires_at is not None and key.expires_at <= now:
            return None
        if not verify_api_key(raw_key, key.key_hash, pepper=settings.api_key_pepper):
            return None
        tenant = session.get(TenantModel, key.tenant_id)
        if tenant is None or tenant.status != "active":
            return None
        key.last_used_at = now
        session.add(key)
        session.commit()
        return AuthenticatedTenant(
            tenant_id=tenant.id,
            tenant_slug=tenant.slug,
            tenant_name=tenant.name,
            api_key_id=key.id,
            allowed_countries=tuple(tenant.allowed_countries or []),
            allowed_modules=tuple(tenant.allowed_modules or []),
        )
