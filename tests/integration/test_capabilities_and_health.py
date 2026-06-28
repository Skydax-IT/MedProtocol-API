from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_is_public(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_landing_page_is_public(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "MedProtocol API" in response.text
    assert "DEMO ONLY" in response.text
    assert "Open Demo UI" in response.text


def test_demo_page_is_public_and_safety_marked(client: TestClient) -> None:
    response = client.get("/demo")

    assert response.status_code == 200
    assert "DEMO ONLY" in response.text
    assert "Do not enter real patient data" in response.text
    assert "Copy JSON response" in response.text
    assert "View audit record" in response.text


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
