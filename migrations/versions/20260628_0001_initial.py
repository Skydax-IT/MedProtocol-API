from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260628_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("allowed_countries", sa.JSON(), nullable=False),
        sa.Column("allowed_modules", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tenants_slug"), "tenants", ["slug"], unique=True)
    op.create_index(op.f("ix_tenants_status"), "tenants", ["status"], unique=False)

    op.create_table(
        "api_keys",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("key_prefix", sa.String(length=32), nullable=False),
        sa.Column("key_hash", sa.Text(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_api_keys_key_prefix"), "api_keys", ["key_prefix"], unique=False)
    op.create_index(op.f("ix_api_keys_status"), "api_keys", ["status"], unique=False)
    op.create_index(op.f("ix_api_keys_tenant_id"), "api_keys", ["tenant_id"], unique=False)

    op.create_table(
        "protocols",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("protocol_id", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("module", sa.String(length=80), nullable=False),
        sa.Column("country_code", sa.String(length=32), nullable=True),
        sa.Column("source_label", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("validation_status", sa.String(length=60), nullable=False),
        sa.Column("clinical_use_status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_protocols_module"), "protocols", ["module"], unique=False)
    op.create_index(op.f("ix_protocols_protocol_id"), "protocols", ["protocol_id"], unique=True)
    op.create_index(op.f("ix_protocols_status"), "protocols", ["status"], unique=False)

    op.create_table(
        "protocol_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("protocol_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=120), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deprecated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["protocol_id"], ["protocols.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("protocol_id", "version", name="uq_protocol_version"),
    )
    op.create_index(
        op.f("ix_protocol_versions_protocol_id"),
        "protocol_versions",
        ["protocol_id"],
        unique=False,
    )

    op.create_table(
        "rules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("rule_id", sa.String(length=160), nullable=False),
        sa.Column("protocol_version_id", sa.String(length=36), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("module", sa.String(length=80), nullable=False),
        sa.Column("patient_group", sa.String(length=80), nullable=True),
        sa.Column("condition", sa.JSON(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        sa.Column("safety", sa.JSON(), nullable=False),
        sa.Column("validation_status", sa.String(length=60), nullable=False),
        sa.Column("clinical_use_status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["protocol_version_id"], ["protocol_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rules_module"), "rules", ["module"], unique=False)
    op.create_index(
        op.f("ix_rules_protocol_version_id"),
        "rules",
        ["protocol_version_id"],
        unique=False,
    )
    op.create_index(op.f("ix_rules_rule_id"), "rules", ["rule_id"], unique=True)

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("audit_id", sa.String(length=80), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("api_key_id", sa.String(length=36), nullable=False),
        sa.Column("request_id", sa.String(length=120), nullable=False),
        sa.Column("external_encounter_id", sa.String(length=160), nullable=True),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("module", sa.String(length=80), nullable=False),
        sa.Column("user_role", sa.String(length=80), nullable=False),
        sa.Column("input_summary", sa.JSON(), nullable=False),
        sa.Column("normalized_input", sa.JSON(), nullable=False),
        sa.Column("triggered_rules", sa.JSON(), nullable=False),
        sa.Column("missing_critical_data", sa.JSON(), nullable=False),
        sa.Column("output", sa.JSON(), nullable=False),
        sa.Column("protocol_metadata", sa.JSON(), nullable=False),
        sa.Column("clinical_use_status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_events_audit_id"), "audit_events", ["audit_id"], unique=True)
    op.create_index(
        op.f("ix_audit_events_api_key_id"), "audit_events", ["api_key_id"], unique=False
    )
    op.create_index(
        op.f("ix_audit_events_country_code"), "audit_events", ["country_code"], unique=False
    )
    op.create_index(op.f("ix_audit_events_module"), "audit_events", ["module"], unique=False)
    op.create_index(
        op.f("ix_audit_events_request_id"), "audit_events", ["request_id"], unique=False
    )
    op.create_index(op.f("ix_audit_events_tenant_id"), "audit_events", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_audit_events_user_role"), "audit_events", ["user_role"], unique=False)
    op.create_index(
        "ix_audit_tenant_audit_id", "audit_events", ["tenant_id", "audit_id"], unique=False
    )

    op.create_table(
        "offline_bundles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("bundle_id", sa.String(length=200), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("module_code", sa.String(length=80), nullable=False),
        sa.Column("manifest", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_offline_bundles_bundle_id"),
        "offline_bundles",
        ["bundle_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_offline_bundles_country_code"),
        "offline_bundles",
        ["country_code"],
        unique=False,
    )
    op.create_index(
        op.f("ix_offline_bundles_module_code"),
        "offline_bundles",
        ["module_code"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_offline_bundles_module_code"), table_name="offline_bundles")
    op.drop_index(op.f("ix_offline_bundles_country_code"), table_name="offline_bundles")
    op.drop_index(op.f("ix_offline_bundles_bundle_id"), table_name="offline_bundles")
    op.drop_table("offline_bundles")
    op.drop_index("ix_audit_tenant_audit_id", table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_user_role"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_tenant_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_request_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_module"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_country_code"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_api_key_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_audit_id"), table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index(op.f("ix_rules_rule_id"), table_name="rules")
    op.drop_index(op.f("ix_rules_protocol_version_id"), table_name="rules")
    op.drop_index(op.f("ix_rules_module"), table_name="rules")
    op.drop_table("rules")
    op.drop_index(op.f("ix_protocol_versions_protocol_id"), table_name="protocol_versions")
    op.drop_table("protocol_versions")
    op.drop_index(op.f("ix_protocols_status"), table_name="protocols")
    op.drop_index(op.f("ix_protocols_protocol_id"), table_name="protocols")
    op.drop_index(op.f("ix_protocols_module"), table_name="protocols")
    op.drop_table("protocols")
    op.drop_index(op.f("ix_api_keys_tenant_id"), table_name="api_keys")
    op.drop_index(op.f("ix_api_keys_status"), table_name="api_keys")
    op.drop_index(op.f("ix_api_keys_key_prefix"), table_name="api_keys")
    op.drop_table("api_keys")
    op.drop_index(op.f("ix_tenants_status"), table_name="tenants")
    op.drop_index(op.f("ix_tenants_slug"), table_name="tenants")
    op.drop_table("tenants")
