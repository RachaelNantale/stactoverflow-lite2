from flask import Flask
from app.views.views import bp
from app.views.answer_views import answer_bp


def create_app(config_name):
    """Method for creating the app"""
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.register_blueprint(bp)
    app.register_blueprint(answer_bp)
    return app
