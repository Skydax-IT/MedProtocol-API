from __future__ import annotations

from app.api.errors import not_found
from app.application.services.serializers import protocol_to_detail, protocol_to_summary
from app.infrastructure.rules.loader import RuleCatalog, load_demo_catalog


class ProtocolService:
    def __init__(self, catalog: RuleCatalog | None = None) -> None:
        self.catalog = catalog or load_demo_catalog()

    def list_protocols(self) -> list[dict[str, object]]:
        protocols = sorted(self.catalog.protocols.values(), key=lambda item: item.protocol_id)
        return [protocol_to_summary(protocol) for protocol in protocols]

    def get_protocol(self, protocol_id: str) -> dict[str, object]:
        protocol = self.catalog.protocols.get(protocol_id)
        if protocol is None:
            raise not_found("PROTOCOL_NOT_FOUND", f"Protocol {protocol_id} was not found.")
        rule_ids = sorted(
            rule.rule_id for rule in self.catalog.rules if rule.protocol_id == protocol_id
        )
        return protocol_to_detail(protocol, rule_ids)
