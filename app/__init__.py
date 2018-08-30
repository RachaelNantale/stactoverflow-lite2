from flask import Flask
from flask_jwt_extended import JWTManager
from app.views.views import bp
from app.views.answer_views import answer_bp
from app.views.user_views import user_bp


def create_app(config_name):
    """Method for creating the app.  
    This is where th Flask app for Stackoverflow-lite 
    is created from"""
    
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'sup3rsecr3t'
    JWTManager(app)

    app.config.from_object(config_name)
    app.register_blueprint(bp)
    app.register_blueprint(answer_bp)
    app.register_blueprint(user_bp)

    return app
