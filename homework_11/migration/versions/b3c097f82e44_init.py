"""Init

Revision ID: b3c097f82e44
Revises: 
Create Date: 2023-09-08 23:38:54.728130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b3c097f82e44"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=20), nullable=False),
        sa.Column("last_name", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=20), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("birthday_date", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contacts_email"), "contacts", ["email"], unique=True)
    op.create_index(
        op.f("ix_contacts_first_name"), "contacts", ["first_name"], unique=False
    )
    op.create_index(
        op.f("ix_contacts_phone_number"), "contacts", ["phone_number"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_contacts_phone_number"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_first_name"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_email"), table_name="contacts")
    op.drop_table("contacts")
    # ### end Alembic commands ###
