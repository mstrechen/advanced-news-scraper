"""Add tag_id in tag_to_article_text

Revision ID: 66711aea7415
Revises: e93d47520512
Create Date: 2020-09-18 01:46:19.520840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66711aea7415'
down_revision = 'e93d47520512'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'tag_to_article_text',
        sa.Column('tag_id', sa.INTEGER, nullable=False),
    )
    op.create_foreign_key(
        'fk_tag_to_article_text_tag_id',
        'tag_to_article_text', 'tags',
        ['tag_id'], ['tag_id']
    )


def downgrade():
    op.drop_constraint('fk_tag_to_article_text_tag_id', 'tag_to_article_text', type_='foreignkey')
    op.drop_column('tag_to_article_text', 'tag_id')
