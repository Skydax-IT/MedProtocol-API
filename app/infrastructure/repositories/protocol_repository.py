from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import ProtocolMetadata, Rule
from app.infrastructure.models import ProtocolModel, ProtocolVersionModel, RuleModel


class ProtocolRepository:
    def upsert_protocols_and_rules(
        self,
        session: Session,
        protocols: Sequence[ProtocolMetadata],
        rules: Sequence[Rule],
    ) -> None:
        for protocol in protocols:
            model = (
                session.execute(
                    select(ProtocolModel).where(ProtocolModel.protocol_id == protocol.protocol_id)
                )
                .scalars()
                .first()
            )
            if model is None:
                model = ProtocolModel(protocol_id=protocol.protocol_id)
            model.title = protocol.title
            model.module = protocol.module
            model.country_code = protocol.country_code
            model.source_label = protocol.source_label
            model.status = protocol.status
            model.validation_status = protocol.validation_status
            model.clinical_use_status = protocol.clinical_use_status
            session.add(model)
            session.flush()

            version = (
                session.execute(
                    select(ProtocolVersionModel).where(
                        ProtocolVersionModel.protocol_id == model.id,
                        ProtocolVersionModel.version == protocol.version,
                    )
                )
                .scalars()
                .first()
            )
            if version is None:
                version = ProtocolVersionModel(protocol_id=model.id, version=protocol.version)
            version.effective_from = self._parse_date(protocol.effective_from)
            version.deprecated_at = self._parse_date(protocol.deprecated_at)
            version.extra_metadata = {
                "validation_status": protocol.validation_status,
                "clinical_use_status": protocol.clinical_use_status,
                "real_care_validation_status": protocol.real_care_validation_status,
                "source_label": protocol.source_label,
            }
            session.add(version)

        session.flush()
        versions_by_key = {
            (version.protocol.protocol_id, version.version): version
            for version in session.execute(select(ProtocolVersionModel)).scalars().all()
        }

        for rule in rules:
            protocol_version = versions_by_key[(rule.protocol_id, rule.protocol_version)]
            model = (
                session.execute(select(RuleModel).where(RuleModel.rule_id == rule.rule_id))
                .scalars()
                .first()
            )
            if model is None:
                model = RuleModel(rule_id=rule.rule_id)
            model.protocol_version_id = protocol_version.id
            model.priority = rule.priority
            model.module = rule.module
            model.patient_group = rule.patient_group
            model.condition = dict(rule.condition)
            model.result = dict(rule.result)
            model.safety = dict(rule.safety)
            model.validation_status = rule.validation_status
            model.clinical_use_status = rule.clinical_use_status
            session.add(model)
        session.commit()

    def _parse_date(self, value: str | None) -> datetime | None:
        if not value:
            return None
        if value.endswith("Z"):
            value = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed
