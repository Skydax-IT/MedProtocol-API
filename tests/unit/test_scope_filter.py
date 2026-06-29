from __future__ import annotations

from app.domain.engine import DecisionEngine
from app.infrastructure.rules.loader import load_demo_catalog


def test_scope_adapter_removes_forbidden_content_markers(
    child_danger_payload: dict[str, object],
) -> None:
    catalog = load_demo_catalog()
    result = DecisionEngine(
        rules=catalog.rules,
        protocols=catalog.protocols,
        country_packs=catalog.country_packs,
        scopes=catalog.scopes,
    ).evaluate(child_danger_payload)

    assert result.scope_role == "community_health_worker"
    assert "diagnosis" in result.forbidden_content_removed
    assert "dosage" in result.forbidden_content_removed
