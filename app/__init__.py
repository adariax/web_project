from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)


def get_db_session() -> db.Session:
    return db.session


login_manager = LoginManager(app)

from app.data import posts_api, users_api

api = Api(app)
api.add_resource(users_api.UsersResource, '/api/users')

app.register_blueprint(users_api.blueprint)
app.register_blueprint(posts_api.blueprint)
