from admin.app import db

from .user import User



class Site(db.Model):
    __tablename__ = 'sites'
    site_id = db.Column(db.INTEGER, primary_key=True)
    base_url = db.Column(db.String(255), unique=True, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    active_parser_id = db.Column(db.INTEGER, db.ForeignKey('site_parsers.parser_id'), nullable=True)


class SiteParser(db.Model):
    __tablename__ = 'site_parsers'
    parser_id = db.Column(db.INTEGER, primary_key=True)
    syntax = db.Column(db.Enum('yaml', 'json'), nullable=False)
    type = db.Column(db.Enum('dynamic', 'static', 'rest_api'), nullable=False)
    has_newslist_parser = db.Column(db.BOOLEAN, nullable=False)
    has_article_parser = db.Column(db.BOOLEAN, nullable=False)
    creator_id = db.Column(db.INTEGER, db.ForeignKey(User.id), nullable=False)
    site_id = db.Column(db.INTEGER, db.ForeignKey(Site.site_id), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    comment = db.Column(db.TEXT, nullable=False, default='')
