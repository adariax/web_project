class Config(object):
    """
    SECRET KEY -- Secure key from VK WEB APP settings

    CLIENT ID -- VK WEB APP ID

    ACCESS TOKEN -- Service token from VK WEB APP

    VK GROUP ID -- ID of group you want to use for site
    """

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
