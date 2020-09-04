from admin.app import db


class Site(db.Model):
    __tablename__ = 'sites'
    site_id = db.Column(db.INTEGER, primary_key=True)
    base_url = db.Column(db.String(255), unique=True, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    active_parser_id = db.Column(db.INTEGER, db.ForeignKey('site_parsers.parser_id'), nullable=True)
