from sqlalchemy.orm import backref

from FlaskProject import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from authlib.jose import jwt, JsonWebSignature
from enum import Enum


class Permission(Enum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    permission = db.Column(db.Enum(Permission), nullable=False, default=Permission.USER)

    def __init__(self, email):
        self.email = email
        self.confirmed = False
        self.permission = Permission.USER

    def generate_conf_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        if data.payload.decode('utf-8') != str(self.id):
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    @property
    def password(self):
        raise AttributeError('Password is not available for reading')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def password_verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


cart_items = db.Table(
    'cart_items',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    picture = db.Column(db.String(255))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    price = db.Column(db.DECIMAL(10, 2))

    def __repr__(self):
        return '<Item %r>' % self.name


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    items = db.relationship('Item', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<Type %r>' % self.type


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
