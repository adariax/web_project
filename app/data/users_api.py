from flask import jsonify, Blueprint, make_response
from flask_restful import Resource
from flask_login import current_user

from app import get_db_session
from app.models import User
from app.data.parser import user_parser as parser
from check_user import is_admin


class UsersResource(Resource):
    def get(self):
        return jsonify(current_user.to_dict())

    def post(self):
        arg = parser.parse_args()
        session = get_db_session()
        if session.query(User).filter(User.vk_domain == arg['vkDomain']).first():
            return make_response(jsonify({'error': 'this VK account has already registered'}), 400)
        user = User(
            nickname=arg['nickname'],
            vk_domain=arg['vkDomain'],
            access_token=arg['accessToken'],
            is_admin=is_admin(arg['vkDomain'], arg['accessToken'])
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


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


@blueprint.route('/api/user/is_admin/<params>')
def check_is_admin(params):
    info = params.split('&')
    return jsonify({'response': True}) if is_admin(*info) else jsonify({"response": False})
