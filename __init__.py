# __init__.py
from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize bcrypt
    bcrypt.init_app(app)

    # Import and register blueprints
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
