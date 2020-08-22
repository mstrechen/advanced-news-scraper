"""Add sites and parsers

Revision ID: 1ea0d053b0cc
Revises: 4f67d2ff97e6
Create Date: 2020-08-22 17:34:44.092390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea0d053b0cc'
down_revision = '4f67d2ff97e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sites',
        sa.Column('site_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('base_url', sa.VARCHAR(length=255), unique=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP, nullable=False),
        sa.Column('active_parser_id', sa.INTEGER, nullable=True),
    )
    op.create_table(
        'site_parsers',
        sa.Column('parser_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('syntax', sa.Enum('yaml', 'json'), nullable=False),
        sa.Column('type', sa.Enum('dynamic', 'static', 'rest_api'), nullable=False),
        sa.Column('has_newslist_parser', sa.BOOLEAN, nullable=False),
        sa.Column('has_article_parser', sa.BOOLEAN, nullable=False),
        sa.Column('creator_id', sa.INTEGER, nullable=False),
        sa.Column('site_id', sa.INTEGER, nullable=False),
        sa.Column('created', sa.TIMESTAMP, nullable=False, server_default=sa.text('NOW()')),
        sa.Column('comment', sa.TEXT, nullable=False, default=''),
    )
    op.create_foreign_key('fk_sites_active_parser_id',
                          'sites', 'site_parsers',
                          ['active_parser_id'], ['parser_id'])

    op.create_foreign_key('fk_site_parsers_site_id',
                          'site_parsers', 'sites',
                          ['site_id'], ['site_id'])

    op.create_foreign_key('fk_site_parsers_creator_id',
                          'site_parsers', 'users',
                          ['creator_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_site_parsers_creator_id', 'site_parsers', type_='foreignkey')
    op.drop_constraint('fk_site_parsers_site_id', 'site_parsers', type_='foreignkey')
    op.drop_constraint('fk_sites_active_parser_id', 'sites', type_='foreignkey')

    op.drop_table('site_parsers')
    op.drop_table('sites')
