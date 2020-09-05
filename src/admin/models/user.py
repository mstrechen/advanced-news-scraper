from flask_login import UserMixin
from flask_security import RoleMixin

from admin.app import db


class UserRole(db.Model, RoleMixin):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name.upper()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    full_name = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
    password = db.Column(db.VARCHAR(255), name='password_hash')
    active = db.Column(db.Boolean(), name='is_active')

    roles = db.relationship('UserRole', secondary='roles_to_users',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return self.full_name


roles_to_users = db.Table(
    'roles_to_users',
    db.Column('user_id', db.Integer(), db.ForeignKey(User.id)),
    db.Column('role_id', db.Integer(), db.ForeignKey(UserRole.id))
)
