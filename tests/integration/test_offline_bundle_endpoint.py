from __future__ import annotations

from fastapi.testclient import TestClient


def test_offline_bundle_returns_manifest(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get("/v1/offline/bundles/CF/child_triage", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["bundle_id"] == "CF-child_triage-DEMO_DRAFT_NOT_VALIDATED"
    assert body["clinical_use_status"] == "not_for_real_patient_care"
    assert body["signature"] == "demo-signature-placeholder"
    child_rule = next(rule for rule in body["rules"] if rule["rule_id"] == "demo_child_danger_001")
    assert child_rule["status"] == "draft"
    assert child_rule["validation_status"] == "demo_only"
    assert child_rule["clinical_use_status"] == "not_for_real_patient_care"
    assert child_rule["real_care_validation_status"] == "not_validated_for_real_care"
