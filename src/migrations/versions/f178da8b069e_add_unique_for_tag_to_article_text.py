"""Add unique for tag_to_article_text

Revision ID: f178da8b069e
Revises: 66711aea7415
Create Date: 2020-09-18 02:17:20.655742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f178da8b069e'
down_revision = '66711aea7415'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        'uq_tag_to_article_text',
        'tag_to_article_text',
        ['text_id', 'rule_id', 'user_id']
    )


def downgrade():
    op.drop_constraint('uq_tag_to_article_text', 'tag_to_article_text', type_='unique')
