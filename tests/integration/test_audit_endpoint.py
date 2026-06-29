from __future__ import annotations

from fastapi.testclient import TestClient


def test_audit_can_be_retrieved_by_same_tenant(
    client: TestClient,
    auth_headers: dict[str, str],
    child_danger_payload: dict[str, object],
) -> None:
    audit_id = client.post(
        "/v1/triage/evaluate",
        headers=auth_headers,
        json=child_danger_payload,
    ).json()["audit_id"]

    response = client.get(f"/v1/audit/{audit_id}", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["audit_id"] == audit_id
    assert body["triggered_rules"] == ["demo_child_danger_001"]
    assert body["normalized_input"]["patient_context"]["patient_ref"] is None


def test_audit_is_tenant_scoped(
    client: TestClient,
    auth_headers: dict[str, str],
    other_auth_headers: dict[str, str],
    child_danger_payload: dict[str, object],
) -> None:
    audit_id = client.post(
        "/v1/triage/evaluate",
        headers=auth_headers,
        json=child_danger_payload,
    ).json()["audit_id"]

    response = client.get(f"/v1/audit/{audit_id}", headers=other_auth_headers)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "AUDIT_NOT_FOUND"
