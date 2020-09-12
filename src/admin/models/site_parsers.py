from admin.app import db

from .sites import Site
from .user import User


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
    rules = db.Column(db.TEXT, nullable=False)
    active = db.Column(db.BOOLEAN, nullable=False)

    site = db.relationship('Site', remote_side=[site_id], backref='parsers')
