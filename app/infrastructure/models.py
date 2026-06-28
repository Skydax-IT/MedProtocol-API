from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.infrastructure.database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(UTC)


class TenantModel(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)
    allowed_countries: Mapped[list[str]] = mapped_column(JSON, default=list)
    allowed_modules: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    api_keys: Mapped[list[APIKeyModel]] = relationship(back_populates="tenant")


class APIKeyModel(Base):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    key_prefix: Mapped[str] = mapped_column(String(32), index=True)
    key_hash: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    tenant: Mapped[TenantModel] = relationship(back_populates="api_keys")


class ProtocolModel(Base):
    __tablename__ = "protocols"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    protocol_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    module: Mapped[str] = mapped_column(String(80), index=True)
    country_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    source_label: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), index=True)
    validation_status: Mapped[str] = mapped_column(String(60))
    clinical_use_status: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    versions: Mapped[list[ProtocolVersionModel]] = relationship(back_populates="protocol")


class ProtocolVersionModel(Base):
    __tablename__ = "protocol_versions"
    __table_args__ = (UniqueConstraint("protocol_id", "version", name="uq_protocol_version"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    protocol_id: Mapped[str] = mapped_column(ForeignKey("protocols.id"), index=True)
    version: Mapped[str] = mapped_column(String(120))
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deprecated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    extra_metadata: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    protocol: Mapped[ProtocolModel] = relationship(back_populates="versions")
    rules: Mapped[list[RuleModel]] = relationship(back_populates="protocol_version")


class RuleModel(Base):
    __tablename__ = "rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    rule_id: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    protocol_version_id: Mapped[str] = mapped_column(ForeignKey("protocol_versions.id"), index=True)
    priority: Mapped[int] = mapped_column(Integer)
    module: Mapped[str] = mapped_column(String(80), index=True)
    patient_group: Mapped[str | None] = mapped_column(String(80), nullable=True)
    condition: Mapped[dict[str, Any]] = mapped_column(JSON)
    result: Mapped[dict[str, Any]] = mapped_column(JSON)
    safety: Mapped[dict[str, Any]] = mapped_column(JSON)
    validation_status: Mapped[str] = mapped_column(String(60))
    clinical_use_status: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    protocol_version: Mapped[ProtocolVersionModel] = relationship(back_populates="rules")


class AuditEventModel(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    audit_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    api_key_id: Mapped[str] = mapped_column(String(36), index=True)
    request_id: Mapped[str] = mapped_column(String(120), index=True)
    external_encounter_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    module: Mapped[str] = mapped_column(String(80), index=True)
    user_role: Mapped[str] = mapped_column(String(80), index=True)
    input_summary: Mapped[dict[str, Any]] = mapped_column(JSON)
    normalized_input: Mapped[dict[str, Any]] = mapped_column(JSON)
    triggered_rules: Mapped[list[str]] = mapped_column(JSON)
    missing_critical_data: Mapped[list[str]] = mapped_column(JSON)
    output: Mapped[dict[str, Any]] = mapped_column(JSON)
    protocol_metadata: Mapped[dict[str, Any]] = mapped_column(JSON)
    clinical_use_status: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


Index("ix_audit_tenant_audit_id", AuditEventModel.tenant_id, AuditEventModel.audit_id)


class OfflineBundleModel(Base):
    __tablename__ = "offline_bundles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    bundle_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    country_code: Mapped[str] = mapped_column(String(2), index=True)
    module_code: Mapped[str] = mapped_column(String(80), index=True)
    manifest: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
