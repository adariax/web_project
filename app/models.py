from app import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash


class Palette(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, index=True, unique=True, nullable=False)
    colors = db.Column(db.String, index=True)

    def __repr__(self):
        return '<Palette {}>'.format(self.title)


class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vk_id = db.Column(db.Integer, index=True, nullable=False)
    photo_url = db.Column(db.String, nullable=False)
    palette = db.Column(db.Integer, db.ForeignKey('palette.id'))

    def __repr__(self):
        return '<Post {} on https://vk.com/squared_fish>'.format(self.vk_id)


class User(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)
    vk_domain = db.Column(db.String, unique=True)
    access_token = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return '<User {}>'.format(self.nickname)
