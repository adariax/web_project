from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('nickname', required=True)
user_parser.add_argument('vkDomain', required=True)
user_parser.add_argument('accessToken', required=True)
