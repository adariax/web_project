from flask import jsonify, Blueprint, make_response
from flask_restful import Resource

from app import get_db_session
from app.models import User


class UsersResource(Resource):
    def get(self):
        session = get_db_session()
        users = session.query(User).all()
        return jsonify({'users': user.to_dict(only=('nickname', 'vk_domain'))
                        for user in users})


blueprint = Blueprint('rest_api', __name__, template_folder='templates')


@blueprint.route('/api/user/login/<login>')
def check_login(login):
    session = get_db_session()
    user = session.query(User).filter(User.nickname == login).first()
    return jsonify({'response': 'user has found'}) if user \
        else make_response(jsonify({"error": "user doesn't exist"}), 404)


@blueprint.route('/api/user/vk_id/<vk_id>')
def check_id(vk_id):
    session = get_db_session()
    user = session.query(User).filter(User.vk_domain == vk_id).first()
    return jsonify({'response': 'current account has already register'}) if user \
        else make_response(jsonify({"error": "account with this id doesn't exist"}), 404)
