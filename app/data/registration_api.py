from flask import jsonify
from flask_restful import Resource

from app import session
from app.data.parser import session_parser as parser


def registration_data_is_empty():
    return False if 'registration' in session else True


class SessionResource(Resource):
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
