""""Initial tables configuration"

Revision ID: 8f176326a337
Revises: 
Create Date: 2020-08-08 00:49:48.276375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f176326a337'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True),
        sa.Column('full_name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )


def downgrade():
    op.drop_table('users')
