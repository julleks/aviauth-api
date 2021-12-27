"""0009 Add backwards relation form User to AccessTokens

Revision ID: 575d6d6b784a
Revises: ea6cf3ae3ecf
Create Date: 2021-12-27 19:08:22.711319

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "575d6d6b784a"
down_revision = "ea6cf3ae3ecf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accesstoken",
        sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.drop_index("ix_accesstoken_is_active", table_name="accesstoken")
    op.drop_column("accesstoken", "is_active")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accesstoken",
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.create_index(
        "ix_accesstoken_is_active", "accesstoken", ["is_active"], unique=False
    )
    op.drop_column("accesstoken", "deactivated_at")
    # ### end Alembic commands ###
