from flask import jsonify, Blueprint, make_response
from flask_restful import Resource
from flask_login import current_user

from app import get_db_session, app
from app.models import User
from app.data.parser import user_parser as parser
from app.data.user import is_admin


class UsersResource(Resource):
    def get(self):
        """
        :return: object with info of current user
        """

        return jsonify(current_user.to_dict())

    def post(self):
        """
        Getting from the request obj with registration info:
        nickname, access token, vk id

        Create User obj and add it into the db.
        """

        arg = parser.parse_args()
        session = get_db_session()
        if session.query(User).filter(User.vk_domain == arg['vkDomain']).first():
            return make_response(jsonify({'error': 'this VK account has already registered'}), 400)
        user = User(
            nickname=arg['nickname'],
            vk_domain=arg['vkDomain'],
            access_token=arg['accessToken'],
            is_admin=is_admin(arg['vkDomain'], arg['accessToken'],
                              int(app.config['VK_GROUP_ID'][1:]))
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


blueprint = Blueprint('users_rest_api', __name__, template_folder='templates')


@blueprint.route('/api/user/nickname/<nickname>')
def check_login(nickname):
    """
    :param nickname: user's entered nickname

    :return: response 404 if user doesn't exist else obj with message about user's existing
    """

    session = get_db_session()
    user = session.query(User).filter(User.nickname == nickname).first()
    return jsonify({'response': 'user has found'}) if user \
        else make_response(jsonify({"error": "user doesn't exist"}), 404)


@blueprint.route('/api/user/vk_id/<vk_id>')
def check_id(vk_id):
    """
    :param vk_id: user's vk id for checking

    :return: response 404 if account doesn't register
             else obj with message about account's registration
    """

    session = get_db_session()
    user = session.query(User).filter(User.vk_domain == vk_id).first()
    return jsonify({'response': 'current account has already register'}) if user \
        else make_response(jsonify({"error": "account with this id doesn't exist"}), 404)
