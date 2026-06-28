from __future__ import annotations

import json
from pathlib import Path

from app.application.services.serializers import decision_to_payload
from app.domain.engine import DecisionEngine
from app.infrastructure.rules.loader import load_demo_catalog


def test_child_danger_output_matches_golden(child_danger_payload: dict[str, object]) -> None:
    catalog = load_demo_catalog()
    result = DecisionEngine(
        rules=catalog.rules,
        protocols=catalog.protocols,
        country_packs=catalog.country_packs,
        scopes=catalog.scopes,
    ).evaluate(child_danger_payload)
    actual = decision_to_payload(result)
    expected = json.loads(
        Path("tests/fixtures/expected_child_danger_output.json").read_text(encoding="utf-8")
    )

    assert actual == expected
