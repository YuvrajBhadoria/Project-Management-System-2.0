"""create organizations and organization_members

Revision ID: 7149bcd83c45
Revises: 
Create Date: 2026-11-16 06:19:16.655601

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7149bcd83c45'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:

    # 1. Create organizations table
    op.create_table(
        "organizations",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()")
        ),

        sa.Column("name", sa.String(100), nullable=False),

        sa.Column("slug", sa.String(100), nullable=False),

        sa.Column("created_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="RESTRICT"),
                  nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP")
        ),

        sa.UniqueConstraint("slug", name="uq_organizations_slug")
    )


    # 2. Create organization_members table
    op.create_table(
        "organization_members",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()")
        ),

        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False
        ),

        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        ),

        sa.Column("role", sa.String(30), nullable=False),

        sa.Column(
            "joined_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP")
        ),

        # A user cannot join the same organization twice
        sa.UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_organization_members_org_user"
        )
    )


def downgrade() -> None:

    # Drop child table first because it references organizations
    op.drop_table("organization_members")

    op.drop_table("organizations")
