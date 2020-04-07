from flask import jsonify
from flask_restful import Resource

from app.models import Post
from app import get_db_session


class PostsResource(Resource):
    def get(self):
        session = get_db_session()
        posts = session.query(Post).all()
        return jsonify({'posts': [post.to_dict(only=('id', 'vk_id', 'photo_url'))
                                  for post in posts]})
