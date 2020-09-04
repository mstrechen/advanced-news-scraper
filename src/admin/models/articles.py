from sqlalchemy.dialects.mysql import MEDIUMTEXT as sa_MEDIUMTEXT
from admin.app import db


class Article(db.Model):
    __tablename__ = 'articles'
    article_id = db.Column(db.INTEGER, primary_key=True)
    site_id = db.Column(db.INTEGER, nullable=False)
    last_text_id = db.Column(db.INTEGER, nullable=True)
    language = db.Column(db.VARCHAR(3), nullable=True)
    url = db.Column(db.VARCHAR(255), nullable=False)


class ArticleText(db.Model):
    __tablename__ = 'article_texts'
    text_id = db.Column(db.INTEGER, primary_key=True)
    article_id = db.Column(db.INTEGER, db.ForeignKey('articles.article_id'), nullable=False)
    parser_id = db.Column(db.INTEGER, db.ForeignKey('site_parsers.parser_id'), nullable=False)
    title = db.Column(db.TEXT, nullable=False)
    content = db.Column(sa_MEDIUMTEXT, nullable=False)
    hash = db.Column(db.VARCHAR(64), nullable=False)

    downloaded = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())


tag_to_article_text = db.Table(
    'tag_to_article_text',
    db.Column('text_id', db.Integer(), db.ForeignKey(ArticleText.text_id)),
    db.Column('article_id', db.Integer(), db.ForeignKey(Article.article_id)),
    db.Column('rule_id', db.Integer(), db.ForeignKey('tag_rules.rule_id'), nullable=True),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=True),
)
