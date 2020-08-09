from admin.app import db


class UserRole:
    ADMIN = 'admin'
    USER = 'user'

    ALL_ROLES = [ADMIN, USER]


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    full_name = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
    role = db.Column(db.Enum(*UserRole.ALL_ROLES))
