class Config(object):
    FLASK_APP = 'main.py'

    SECRET_KEY = ''
    CLIENT_ID = ''
    ACCESS_TOKEN = ''

    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    VK_GROUP_ID = ''


class DevConfig(Config):
    TESTING = False
    DEBUG = True
