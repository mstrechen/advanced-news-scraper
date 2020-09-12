"""site_parser active column

Revision ID: e93d47520512
Revises: a8fddc56f362
Create Date: 2020-09-12 10:39:34.211145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e93d47520512'
down_revision = 'a8fddc56f362'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('site_parsers', sa.Column('active', sa.BOOLEAN, nullable=False))


def downgrade():
    op.drop_column('site_parsers', 'active')
