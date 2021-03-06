"""0002 Create Access Token model

Revision ID: a899a4a9c223
Revises: f24488b5f75c
Create Date: 2021-12-25 22:46:50.039338

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "a899a4a9c223"
down_revision = "f24488b5f75c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accesstoken",
        sa.Column("access_token", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("token_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("scope", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("access_token"),
    )
    op.create_index(
        op.f("ix_accesstoken_access_token"),
        "accesstoken",
        ["access_token"],
        unique=True,
    )
    op.create_index(
        op.f("ix_accesstoken_created_at"), "accesstoken", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_accesstoken_expires_at"), "accesstoken", ["expires_at"], unique=False
    )
    op.create_index(
        op.f("ix_accesstoken_is_active"), "accesstoken", ["is_active"], unique=False
    )
    op.create_index(
        op.f("ix_accesstoken_token_type"), "accesstoken", ["token_type"], unique=False
    )
    op.create_index(
        op.f("ix_accesstoken_user_id"), "accesstoken", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_accesstoken_user_id"), table_name="accesstoken")
    op.drop_index(op.f("ix_accesstoken_token_type"), table_name="accesstoken")
    op.drop_index(op.f("ix_accesstoken_is_active"), table_name="accesstoken")
    op.drop_index(op.f("ix_accesstoken_expires_at"), table_name="accesstoken")
    op.drop_index(op.f("ix_accesstoken_created_at"), table_name="accesstoken")
    op.drop_index(op.f("ix_accesstoken_access_token"), table_name="accesstoken")
    op.drop_table("accesstoken")
    # ### end Alembic commands ###
