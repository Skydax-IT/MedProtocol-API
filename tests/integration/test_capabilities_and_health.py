from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_is_public(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_checks_database_and_demo_rules(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["environment"] == "local"
    assert body["checks"] == {
        "api": "ok",
        "database": "ok",
        "demo_rules": "ok",
    }


def test_landing_page_is_public(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "MedProtocol API" in response.text
    assert "Clinical protocol logic, ready for frontline systems" in response.text
    assert "A protocol-based triage layer for frontline health systems" in response.text
    assert "Try the guided demo" in response.text
    assert "The gap in digital health is not data collection" in response.text
    assert "A protocol layer that plugs into existing systems" in response.text
    assert "Demo UX version" in response.text
    assert "polished business demo" in response.text
    assert "demo only" in response.text.lower()
    assert "No real patient data" in response.text
    assert "ready for real patient care" not in response.text.lower()
    assert "safe for real patient care" not in response.text.lower()


def test_guided_demo_page_is_public_and_safety_marked(client: TestClient) -> None:
    response = client.get("/guided-demo")

    assert response.status_code == 200
    assert "Guided product walkthrough" in response.text
    assert "Step 1 — Field observation" in response.text
    assert "Step 2 — Protocol engine result" in response.text
    assert "Step 3 — Traceability" in response.text
    assert "Technical details for developers" in response.text
    assert "Fake cases only" in response.text
    assert "What the field worker observes" in response.text
    assert "What MedProtocol checks" in response.text
    assert "demo only" in response.text.lower()
    assert "Fake cases only" in response.text
    assert "No real patient data" in response.text
    assert "ready for real patient care" not in response.text.lower()
    assert "safe for real patient care" not in response.text.lower()


def test_demo_page_is_public_and_safety_marked(client: TestClient) -> None:
    response = client.get("/demo")

    assert response.status_code == 200
    assert "Technical Demo Console" in response.text
    assert "This page is for developers and technical reviewers." in response.text
    assert "demo only" in response.text.lower()
    assert "No real patient data" in response.text
    assert "Copy JSON response" in response.text
    assert "View audit record" in response.text
    assert "ready for real patient care" not in response.text.lower()
    assert "safe for real patient care" not in response.text.lower()


def test_swagger_docs_are_still_available(client: TestClient) -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_version_exposes_api_and_demo_versions(client: TestClient) -> None:
    response = client.get("/version")

    assert response.status_code == 200
    body = response.json()
    assert body["api_version"] == "0.1.0"
    assert body["demo_version"] == "0.4.0"
    assert body["product_stage"] == "prototype"
    assert body["clinical_status"] == "demo_only_not_validated"


def test_public_pages_do_not_claim_real_clinical_use(client: TestClient) -> None:
    prohibited_phrases = [
        "provides diagnosis",
        "provides a diagnosis",
        "validated clinical product",
        "ready for real patient care",
        "safe for real patient care",
        "treatment recommendation engine",
    ]

    for route in ["/", "/guided-demo", "/demo", "/docs"]:
        response = client.get(route)
        assert response.status_code == 200
        page = response.text.lower()
        for phrase in prohibited_phrases:
            assert phrase not in page


def test_capabilities_require_auth(client: TestClient) -> None:
    response = client.get("/v1/capabilities")

    assert response.status_code == 401


def test_capabilities_lists_supported_demo_assets(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get("/v1/capabilities", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["countries"] == ["CF", "TD"]
    assert "community_health_worker" in body["roles"]
    assert body["clinical_use_status"] == "not_for_real_patient_care"
