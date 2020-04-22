from app import db, app
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

fav_posts = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                     )


class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vk_id = db.Column(db.Integer, index=True, nullable=False)
    photo_url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Post {} on https://vk.com/{}>'.format(self.vk_id,
                                                       app.config['VK_GROUP_SCREEN_NAME'])


class User(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String, unique=True)
    vk_domain = db.Column(db.String, unique=True)
    access_token = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean)

    favors = db.relationship('Post', secondary=fav_posts, backref=db.backref('users'))

    def __repr__(self):
        return '<User {}>'.format(self.nickname)
