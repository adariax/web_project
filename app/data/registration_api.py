from flask import jsonify
from flask_restful import Resource

from app import session
from app.data.parser import session_parser as parser, access_token_parser


def registration_data_is_empty():
    return False if 'registration' in session else True


class RegistrationSessionResource(Resource):
    def get(self):
        if registration_data_is_empty():
            return jsonify({'error': 'registration data is empty'})
        return jsonify({'login': session.get('login'),
                        'password': session.get('password'),
                        'password_again': session.get('password_again')})

    def delete(self):
        session.pop('login', None)
        session.pop('password', None)
        session.pop('password_again', None)
        session.pop('registration', None)
        return jsonify({'success': 'OK'})

    def put(self):
        args = parser.parse_args()
        session['login'] = args['login']
        session['password'] = args['password']
        session['password_again'] = args['password_again']
        return jsonify({'success': 'OK'})

    def post(self):
        args = parser.parse_args()
        session['registration'] = True
        session['login'] = args['login']
        session['password'] = args['password']
        session['password_again'] = args['password_again']
        return jsonify({'success': 'OK'})


class AccessTokenResource(Resource):
    def get(self):
        return jsonify({'access_token': session['access_token'],
                        'user_id': session['user_id']})

    def post(self):
        args = access_token_parser.parse_args()
        session['access_token'] = args['access_token']
        session['user_id'] = args['user_id']
        return jsonify({'success': 'OK'})

    def delete(self):
        session.pop('access_token', None)
        session.pop('user_id', None)
        return jsonify({'success': 'OK'})
