from sqlalchemy import event
from sqlalchemy.dialects.mysql import MEDIUMTEXT as sa_MEDIUMTEXT
from sqlalchemy.engine import Connection

from admin.app import db
from .articles_es import ArticleTextEs


class Article(db.Model):
    __tablename__ = 'articles'
    article_id = db.Column(db.INTEGER, primary_key=True)
    site_id = db.Column(db.INTEGER, nullable=False)
    last_text_id = db.Column(db.INTEGER, db.ForeignKey('article_texts.text_id'), nullable=True)
    language = db.Column(db.VARCHAR(3), nullable=True)
    url = db.Column(db.VARCHAR(255), nullable=False)

    text = db.relationship(
        'ArticleText',
        uselist=False,
        foreign_keys=[last_text_id]
    )


class ArticleText(db.Model):
    __tablename__ = 'article_texts'
    text_id = db.Column(db.INTEGER, primary_key=True)
    article_id = db.Column(db.INTEGER, db.ForeignKey('articles.article_id'), nullable=False)
    parser_id = db.Column(db.INTEGER, db.ForeignKey('site_parsers.parser_id'), nullable=False)
    title = db.Column(db.TEXT, nullable=False)
    content = db.Column(sa_MEDIUMTEXT, nullable=False)
    hash = db.Column(db.VARCHAR(64), nullable=False)

    downloaded = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())

    article = db.relationship('Article', foreign_keys=[article_id], uselist=False)


tag_to_article_text = db.Table(
    'tag_to_article_text',
    db.Column('text_id', db.Integer(), db.ForeignKey(ArticleText.text_id)),
    db.Column('article_id', db.Integer(), db.ForeignKey(Article.article_id)),
    db.Column('rule_id', db.Integer(), db.ForeignKey('tag_rules.rule_id'), nullable=True),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=True),
)


@event.listens_for(Article, 'after_insert')
@event.listens_for(Article, 'after_update')
def article_on_create_or_update(mapper, connection, article: Article):
    es_entity = ArticleTextEs(
        meta={'id': article.article_id},
        site_id=article.site_id,
        language=article.language,
        url=article.url,
        content=article.text.content if article.text else None,
        title=article.text.title if article.text else None,
    )
    es_entity.save()


@event.listens_for(ArticleText, 'after_insert')
@event.listens_for(ArticleText, 'after_update')
def article_text_on_create_or_update(mapper, connection: Connection, article_text: ArticleText):
    article = db.session.query(Article) \
        .filter(Article.article_id == article_text.article_id) \
        .one()
    article.text = article_text
    article_on_create_or_update(mapper, connection, article)
