from __future__ import annotations

from sqlalchemy import select

from app.config import get_settings
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import APIKeyModel, TenantModel
from app.infrastructure.repositories.protocol_repository import ProtocolRepository
from app.infrastructure.rules.loader import load_demo_catalog
from app.infrastructure.security.hashing import api_key_prefix, hash_api_key


def seed() -> None:
    settings = get_settings()
    catalog = load_demo_catalog()
    with SessionLocal() as session:
        tenant = (
            session.execute(
                select(TenantModel).where(TenantModel.slug == settings.demo_tenant_slug)
            )
            .scalars()
            .first()
        )
        if tenant is None:
            tenant = TenantModel(
                slug=settings.demo_tenant_slug,
                name="Demo Tenant",
                status="active",
                allowed_countries=["CF", "TD"],
                allowed_modules=["general_triage", "child_triage", "pregnancy_triage"],
            )
            session.add(tenant)
            session.flush()
        else:
            tenant.status = "active"
            tenant.allowed_countries = ["CF", "TD"]
            tenant.allowed_modules = ["general_triage", "child_triage", "pregnancy_triage"]

        prefix = api_key_prefix(settings.demo_api_key)
        key = (
            session.execute(select(APIKeyModel).where(APIKeyModel.key_prefix == prefix))
            .scalars()
            .first()
        )
        if key is None:
            key = APIKeyModel(
                tenant_id=tenant.id,
                key_prefix=prefix,
                key_hash=hash_api_key(settings.demo_api_key),
                name="Local demo key",
                status="active",
            )
            session.add(key)
        else:
            key.tenant_id = tenant.id
            key.key_hash = hash_api_key(settings.demo_api_key)
            key.status = "active"
            key.revoked_at = None
        session.commit()

        ProtocolRepository().upsert_protocols_and_rules(
            session=session,
            protocols=list(catalog.protocols.values()),
            rules=list(catalog.rules),
        )

    print("Seeded demo tenant, hashed API key, protocols, and demo rules.")
    print(f"Demo tenant slug: {settings.demo_tenant_slug}")
    print(f"Demo API key for local use: {settings.demo_api_key}")


if __name__ == "__main__":
    seed()
