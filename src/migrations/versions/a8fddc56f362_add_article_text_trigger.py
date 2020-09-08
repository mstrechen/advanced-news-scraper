"""Add article text trigger

Revision ID: a8fddc56f362
Revises: c932489956a3
Create Date: 2020-09-08 21:47:49.978332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8fddc56f362'
down_revision = 'c932489956a3'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TRIGGER `update_latest_article_text` AFTER INSERT ON `article_texts`
    FOR EACH ROW
       UPDATE articles
       SET last_text_id = NEW.text_id
       WHERE articles.article_id = NEW.article_id;
    """)


def downgrade():
    op.execute("""
        DROP TRIGGER update_latest_article_text;
    """)
