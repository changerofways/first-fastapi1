"""add last few columns to posts

Revision ID: 8672b5a18ca8
Revises: c59e1890cc29
Create Date: 2023-07-06 22:41:50.214027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8672b5a18ca8'
down_revision = 'c59e1890cc29'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable= False, server_default="True"),)
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable = False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts',"created_at")
    pass
