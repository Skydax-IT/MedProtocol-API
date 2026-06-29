from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ["MEDPROTOCOL_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["MEDPROTOCOL_DEMO_API_KEY"] = "mp_test_demo_local_only_change_me"
os.environ["DEMO_API_KEY"] = "mp_test_demo_local_only_change_me"
os.environ["APP_ENV"] = "local"
os.environ["API_KEY_PEPPER"] = ""

from app.infrastructure.database import Base, SessionLocal, engine  # noqa: E402
from app.infrastructure.models import APIKeyModel, TenantModel  # noqa: E402
from app.infrastructure.repositories.protocol_repository import ProtocolRepository  # noqa: E402
from app.infrastructure.rules.loader import load_demo_catalog  # noqa: E402
from app.infrastructure.security.hashing import api_key_prefix, hash_api_key  # noqa: E402
from app.main import app  # noqa: E402

API_KEY = "mp_test_demo_local_only_change_me"
OTHER_API_KEY = "mp_test_other_tenant_key"


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    catalog = load_demo_catalog()
    with SessionLocal() as session:
        tenant = TenantModel(
            slug="tenant_demo",
            name="Demo Tenant",
            status="active",
            allowed_countries=["CF", "TD"],
            allowed_modules=["general_triage", "child_triage", "pregnancy_triage"],
        )
        other_tenant = TenantModel(
            slug="tenant_other",
            name="Other Tenant",
            status="active",
            allowed_countries=["CF"],
            allowed_modules=["general_triage", "child_triage", "pregnancy_triage"],
        )
        session.add_all([tenant, other_tenant])
        session.flush()
        session.add_all(
            [
                APIKeyModel(
                    tenant_id=tenant.id,
                    key_prefix=api_key_prefix(API_KEY),
                    key_hash=hash_api_key(API_KEY),
                    name="test key",
                    status="active",
                ),
                APIKeyModel(
                    tenant_id=other_tenant.id,
                    key_prefix=api_key_prefix(OTHER_API_KEY),
                    key_hash=hash_api_key(OTHER_API_KEY),
                    name="other key",
                    status="active",
                ),
            ]
        )
        session.commit()
        ProtocolRepository().upsert_protocols_and_rules(
            session=session,
            protocols=list(catalog.protocols.values()),
            rules=list(catalog.rules),
        )
    yield


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    return {"X-API-Key": API_KEY, "X-Request-ID": "req_test_001"}


@pytest.fixture()
def other_auth_headers() -> dict[str, str]:
    return {"X-API-Key": OTHER_API_KEY, "X-Request-ID": "req_test_other"}


@pytest.fixture()
def child_danger_payload() -> dict[str, object]:
    return {
        "patient_context": {
            "patient_ref": None,
            "age_months": 24,
            "sex": "female",
            "pregnancy_status": "not_applicable",
        },
        "encounter_context": {
            "country_code": "CF",
            "region_code": None,
            "setting": "rural_health_post",
            "user_role": "community_health_worker",
            "connectivity": "offline_capable",
            "language": "fr",
        },
        "clinical_inputs": {
            "main_complaint": "fever",
            "duration_days": 2,
            "danger_signs": {
                "convulsions": False,
                "lethargy_or_unconscious": True,
                "unable_to_drink_or_breastfeed": True,
                "respiratory_distress": False,
                "severe_bleeding": False,
            },
            "vitals": {
                "temperature_c": 39.2,
                "respiratory_rate": None,
                "heart_rate": None,
            },
        },
        "resources_available": {
            "referral_transport_available": False,
            "phone_network_available": True,
            "rapid_malaria_test_available": True,
            "ors_available": True,
        },
        "client_context": {
            "external_encounter_id": "external-demo-001",
            "channel": "tablet_app",
            "client_timestamp": "2026-06-28T12:00:00Z",
        },
    }
