from __future__ import annotations

from fastapi.testclient import TestClient


def test_protocols_endpoint_lists_demo_protocols(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get("/v1/protocols", headers=auth_headers)

    assert response.status_code == 200
    ids = {item["protocol_id"] for item in response.json()["items"]}
    assert "demo_child_danger_signs" in ids


def test_protocol_detail_includes_rule_ids(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get("/v1/protocols/demo_child_danger_signs", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["validation_status"] == "demo_only"
    assert body["clinical_use_status"] == "not_for_real_patient_care"
    assert body["rule_ids"] == ["demo_child_danger_001"]
