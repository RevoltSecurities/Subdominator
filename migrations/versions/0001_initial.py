"""initial schema"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "enumeration_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("root_domain", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_enumeration_runs_root_domain", "enumeration_runs", ["root_domain"])

    op.create_table(
        "findings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("enumeration_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("root_domain", sa.String(length=255), nullable=False),
        sa.Column("subdomain", sa.String(length=255), nullable=False),
        sa.Column("resource", sa.String(length=64), nullable=False),
        sa.Column("query_target", sa.String(length=255), nullable=False),
        sa.Column("recursion_depth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("discovered_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("root_domain", "subdomain", name="uq_root_subdomain"),
    )
    op.create_index("ix_findings_root_domain", "findings", ["root_domain"])
    op.create_index("ix_findings_subdomain", "findings", ["subdomain"])
    op.create_index("ix_findings_resource", "findings", ["resource"])


def downgrade() -> None:
    op.drop_index("ix_findings_resource", table_name="findings")
    op.drop_index("ix_findings_subdomain", table_name="findings")
    op.drop_index("ix_findings_root_domain", table_name="findings")
    op.drop_table("findings")
    op.drop_index("ix_enumeration_runs_root_domain", table_name="enumeration_runs")
    op.drop_table("enumeration_runs")
