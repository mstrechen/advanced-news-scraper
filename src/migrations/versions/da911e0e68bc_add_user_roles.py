"""add_user_roles

Revision ID: da911e0e68bc
Revises: 8f176326a337
Create Date: 2020-08-09 23:00:56.671372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da911e0e68bc'
down_revision = '8f176326a337'
branch_labels = None
depends_on = None

ROLES = ['admin', 'user']


def upgrade():
    op.add_column('users', sa.Column('role', sa.Enum(*ROLES), default='user'))


def downgrade():
    op.drop_column('users', 'role')
