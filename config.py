class Config(object):
    FLASK_APP = 'main.py'
    SECRET_KEY = 'SWXSVqXuaKUGhNSbLKIK'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    VK_ACCESS_TOKEN = 'abb213b4abb213b4abb213b449abc27f06aabb2abb213b4f538bde403c220e6ff51b12f'
    VK_GROUP_ID = '-112055138'


class DevConfig(Config):
    TESTING = False
    DEBUG = True
