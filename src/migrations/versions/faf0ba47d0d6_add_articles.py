"""Add articles

Revision ID: faf0ba47d0d6
Revises: 1ea0d053b0cc
Create Date: 2020-08-22 19:03:14.632842

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import MEDIUMTEXT as sa_MEDIUMTEXT


# revision identifiers, used by Alembic.
revision = 'faf0ba47d0d6'
down_revision = '1ea0d053b0cc'
branch_labels = None
depends_on = None


def upgrade():
    '''
Table "articles" {
  "article_id" int(11) [pk, not null, increment]
  "site_id" int(11) [not null]
  "last_text_id" int(11) [null]
  "language" VARCHAR(3) [null]
  "url" VARCHAR(255) [not null, note: "Should it be TEXT?"]
}

Table article_texts {
  "text_id" int(11) [pk, not null, increment]
  "article_id" int(11) [not null]
  "parser_id" int(11) [not null]

  "title" TEXT [not null]
  "content" MEDIUMTEXT [not null]
  "hash" VARCHAR(64) [not null]

  "downloaded" timestamp [default: `now()`, not null]
}


Ref: "articles"."site_id" > "sites"."site_id"
Ref: "article_texts"."parser_id" > "site_parsers"."parser_id"
Ref: "article_texts"."article_id" > "articles"."article_id"
'''
    op.create_table(
        'articles',
        sa.Column('article_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('site_id', sa.INTEGER, nullable=False),
        sa.Column('last_text_id', sa.INTEGER, nullable=True),
        sa.Column('language', sa.VARCHAR(3), nullable=True),
        sa.Column('url', sa.VARCHAR(255), nullable=False),
    )
    op.create_table(
        'article_texts',
        sa.Column('text_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('article_id', sa.INTEGER, nullable=False),
        sa.Column('parser_id', sa.INTEGER, nullable=False),

        sa.Column('title', sa.TEXT, nullable=False),
        sa.Column('content', sa_MEDIUMTEXT, nullable=False),
        sa.Column('hash', sa.VARCHAR(64), nullable=False),

        sa.Column('downloaded', sa.TIMESTAMP, nullable=False, server_default=sa.func.now())
    )
    op.create_foreign_key('fk_articles_site_id',
                          'articles', 'sites',
                          ['site_id'], ['site_id'])

    op.create_foreign_key('fk_article_texts_parser_id',
                          'article_texts', 'site_parsers',
                          ['parser_id'], ['parser_id'])

    op.create_foreign_key('fk_article_texts_article_id',
                          'article_texts', 'articles',
                          ['article_id'], ['article_id'])

    op.create_foreign_key('fk_articles_last_text_id',
                          'articles', 'article_texts',
                          ['last_text_id'], ['text_id'])


def downgrade():
    op.drop_constraint('fk_articles_last_text_id', 'articles', type_='foreignkey')
    op.drop_constraint('fk_article_texts_parser_id', 'article_texts', type_='foreignkey')
    op.drop_constraint('fk_article_texts_article_id', 'article_texts', type_='foreignkey')
    op.drop_constraint('fk_articles_site_id', 'articles', type_='foreignkey')

    op.drop_table('article_texts')
    op.drop_table('articles')
