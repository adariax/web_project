from flask_restful import reqparse, inputs

session_parser = reqparse.RequestParser()
session_parser.add_argument('login', required=True)
session_parser.add_argument('password', required=True)
session_parser.add_argument('password_again', required=True)

