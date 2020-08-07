from admin.app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    full_name = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
