class Config(object):
    FLASK_APP = 'main.py'
    SECRET_KEY = 'SWXSVqXuaKUGhNSbLKIK'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    TESTING = False
    DEBUG = True
