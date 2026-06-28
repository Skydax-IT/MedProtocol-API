from __future__ import annotations

from app.domain.missing_data import MissingDataDetector


def test_missing_data_detector_reports_child_critical_fields(
    child_danger_payload: dict[str, object],
) -> None:
    missing = MissingDataDetector().detect(child_danger_payload)

    assert "weight_kg" in missing
    assert "respiratory_rate" in missing
    assert "age_months" not in missing
