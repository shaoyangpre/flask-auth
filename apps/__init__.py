from flask import Flask
from apps.auth import auth as auth_blueprint


def register_blueprints(app):
    app.register_blueprint(auth_blueprint, url_prefix = '/api')

def register_plugin(app):
    from apps.models import db
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

def creat_app():
    app = Flask(__name__)

    app.config.from_object('apps.config')

    register_blueprints(app)
    register_plugin(app)

    return app