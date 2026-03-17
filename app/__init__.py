from flask import Flask
from config.settings import Config

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # Register blueprints
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
