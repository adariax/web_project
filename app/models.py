from app import db


class Palette(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    slug = db.Column(db.String, index=True, unique=True)
    colors = db.Column(db.String, index=True)

    def __repr__(self):
        return '<Palette {}>'.format(self.title)
