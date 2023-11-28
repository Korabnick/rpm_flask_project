from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

metadata = db.metadata

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

class User(UserMixin, db.Model):    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    _password = db.Column('password', db.String(300), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        try:
            return check_password_hash(self._password, password)
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rental_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic'))
    location = db.relationship('Location', backref=db.backref('favorites', lazy='dynamic'))

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
