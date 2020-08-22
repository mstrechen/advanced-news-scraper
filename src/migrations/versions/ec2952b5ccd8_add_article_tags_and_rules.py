"""Add article tags and rules

Revision ID: ec2952b5ccd8
Revises: faf0ba47d0d6
Create Date: 2020-08-22 19:26:12.078847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec2952b5ccd8'
down_revision = 'faf0ba47d0d6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('tag_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('parent_tag_id', sa.INTEGER, nullable=True),
        sa.Column('name', sa.VARCHAR(255), nullable=False),
        sa.UniqueConstraint('name', 'parent_tag_id'),
    )
    op.create_foreign_key('fk_tags_parent_tag_id',
                          'tags', 'tags',
                          ['parent_tag_id'], ['tag_id'])

    op.create_table(
        'tag_rules',
        sa.Column('rule_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('tag_id', sa.INTEGER, nullable=False),
        sa.Column('rule_type', sa.Enum('es_query', 'keyword_list', 'machine_learning')),
        sa.Column('rule_language', sa.VARCHAR(3), nullable=False),
        sa.Column('rule_query', sa.TEXT, nullable=False),
        sa.Column('creator_id', sa.INTEGER, nullable=False),
        sa.Column('enabled_timestamp', sa.TIMESTAMP, nullable=False, default=sa.func.now()),
        sa.Column('disabled_timestamp', sa.TIMESTAMP, nullable=True),
    )
    op.create_foreign_key('fk_tag_rules_tag_id',
                          'tag_rules', 'tags',
                          ['tag_id'], ['tag_id'])
    op.create_foreign_key('fk_tag_rules_creator_id',
                          'tag_rules', 'users',
                          ['creator_id'], ['id'])

    op.create_table(
        'tag_to_article_text',
        sa.Column('tag_to_article_text_id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('text_id', sa.INTEGER, nullable=False),
        sa.Column('article_id', sa.INTEGER, nullable=False),
        sa.Column('rule_id', sa.INTEGER, nullable=True,
                  comment="NULL means it's a manual tag"),
        sa.Column('user_id', sa.INTEGER, nullable=True,
                  comment="NULL means it's an automatic tag"),
        sa.Column('inverse_tag', sa.BOOLEAN, nullable=False,
                  comment="Inverse tag means that article SHOULD NOT have such a tag."
                          " It also have an advantage over regular tag marks"),
        sa.Column('created', sa.TIMESTAMP, default=sa.func.now()),
    )
    op.create_foreign_key('fk_tag_to_article_text_text_id',
                          'tag_to_article_text', 'article_texts',
                          ['text_id'], ['text_id'])
    op.create_foreign_key('fk_tag_to_article_text_article_id',
                          'tag_to_article_text', 'articles',
                          ['article_id'], ['article_id'])
    op.create_foreign_key('fk_tag_to_article_text_rule_id',
                          'tag_to_article_text', 'tag_rules',
                          ['rule_id'], ['rule_id'])
    op.create_foreign_key('fk_tag_to_article_text_user_id',
                          'tag_to_article_text', 'users',
                          ['user_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_tag_to_article_text_user_id', 'tag_to_article_text', type_='foreignkey')
    op.drop_constraint('fk_tag_to_article_text_rule_id', 'tag_to_article_text', type_='foreignkey')
    op.drop_constraint('fk_tag_to_article_text_article_id', 'tag_to_article_text', type_='foreignkey')
    op.drop_constraint('fk_tag_to_article_text_text_id', 'tag_to_article_text', type_='foreignkey')
    op.drop_table('tag_to_article_text')

    op.drop_constraint('fk_tag_rules_creator_id', 'tag_rules', type_='foreignkey')
    op.drop_constraint('fk_tag_rules_tag_id', 'tag_rules', type_='foreignkey')
    op.drop_table('tag_rules')

    op.drop_constraint('fk_tags_parent_tag_id', 'tags', type_='foreignkey')
    op.drop_table('tags')


