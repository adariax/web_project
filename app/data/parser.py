from flask_restful import reqparse, inputs

session_parser = reqparse.RequestParser()
session_parser.add_argument('login', required=True)
session_parser.add_argument('password', required=True)
session_parser.add_argument('password_again', required=True)

access_token_parser = reqparse.RequestParser()
access_token_parser.add_argument('access_token', required=True)
access_token_parser.add_argument('user_id', required=True)
