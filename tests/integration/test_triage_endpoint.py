from __future__ import annotations

from fastapi.testclient import TestClient


def test_evaluate_triage_creates_audit(
    client: TestClient,
    auth_headers: dict[str, str],
    child_danger_payload: dict[str, object],
) -> None:
    response = client.post("/v1/triage/evaluate", headers=auth_headers, json=child_danger_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["audit_id"].startswith("aud_")
    assert body["urgency_level"] == "urgent_referral"
    assert body["source"]["rule_ids"] == ["demo_child_danger_001"]
    assert body["meta"]["clinical_use_status"] == "not_for_real_patient_care"


def test_evaluate_requires_api_key(
    client: TestClient,
    child_danger_payload: dict[str, object],
) -> None:
    response = client.post("/v1/triage/evaluate", json=child_danger_payload)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
