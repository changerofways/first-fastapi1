"""add_content_column_to_post

Revision ID: 2b5a582d1b57
Revises: 95b2c03e3596
Create Date: 2023-07-06 22:16:06.979595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b5a582d1b57'
down_revision = '5e58b37dd475'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts',"content")
    pass
