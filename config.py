class Config(object):
    FLASK_APP = 'main.py'
    SECRET_KEY = 'SWXSVqXuaKUGhNSbLKIK'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    VK_ACCESS_TOKEN = '2939ee002939ee002939ee00be2948c307229392939ee0077a3b06cba01662e5b207add'
    VK_GROUP_ID = '-193140435'  # '-112055138'
    VK_CLIENT_ID = '7417095'


class DevConfig(Config):
    TESTING = False
    DEBUG = True
