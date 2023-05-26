from flask import Flask
import os
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from

from .auth import auth
from .extensions import db
from .config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            SWAGGER={
                'title': "Flask APIs",
                'uiversion': 3
            }
        )

    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

    app.register_blueprint(auth)
    JWTManager(app)
    Swagger(app, template=template, config=swagger_config)

    @app.errorhandler(404)
    def handle_404(e):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(500)
    def handle_404(e):
        return {'error': 'Internal Server Error'}, 404

    return app