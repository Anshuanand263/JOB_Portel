from flask import Flask
from .config import Config
from .extensions import mongo
from .routes.auth import auth_bp
from .routes.providers import providers_bp
from .routes.users import users_bp
from .routes.common import common_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(providers_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(common_bp)

    return app


