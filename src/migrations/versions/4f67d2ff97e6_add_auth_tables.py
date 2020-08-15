"""add_auth_tables

Revision ID: 4f67d2ff97e6
Revises: da911e0e68bc
Create Date: 2020-08-14 21:12:12.474828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f67d2ff97e6'
down_revision = 'da911e0e68bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=255), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))

    op.create_table(
        'user_roles',
        sa.Column('id', sa.Integer(), autoincrement=True),
        sa.Column('name', sa.VARCHAR(length=80), unique=True, nullable=False),
        sa.Column('description', sa.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'roles_to_users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.UniqueConstraint('user_id', 'role_id'),
        sa.ForeignKeyConstraint(('user_id',), ('users.id',)),
        sa.ForeignKeyConstraint(('role_id',), ('user_roles.id',)),
    )


def downgrade():
    op.drop_table('roles_to_users')
    op.drop_table('user_roles')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'is_active')

