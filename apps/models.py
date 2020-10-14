from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, default='', index=True)
    _password = db.Column('password', db.String(255), default='')
    email = db.Column(String(50), unique=True)
    phone = db.Column(String(11), unique=True)
    is_active = db.Column(SmallInteger, default=0)
    is_superuser = db.Column(SmallInteger, default=0)
    last_login = db.Column(DateTime, default=datetime.now)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    description = Column(String(50))


class Permission(db.Model):
    __tablename__ = "permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    description = Column(String(50))
    endpoint = Column(String(50), unique=True)


class UserRole(db.Model):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    user = db.relationship('User', backref=db.backref('UserRole'))
    role = db.relationship('Role', backref=db.backref('UserRole'))


class RolePermission(db.Model):
    __tablename__ = "role_permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    role = db.relationship('Role', backref=db.backref('RolePermission'))
    permission = db.relationship('Permission', backref=db.backref('RolePermission'))


class UserPermission(db.Model):
    __tablename__ = "user_permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    user = db.relationship('User', backref=db.backref('UserPermission'))
    permission = db.relationship('Permission', backref=db.backref('UserPermission'))