"""site_parser rules column

Revision ID: c932489956a3
Revises: ec2952b5ccd8
Create Date: 2020-09-05 21:18:33.500288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c932489956a3'
down_revision = 'ec2952b5ccd8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('site_parsers', sa.Column('rules', sa.TEXT, nullable=False))


def downgrade():
    op.drop_column('site_parsers', 'rules')
