from app import db
from sqlalchemy_serializer import SerializerMixin


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
