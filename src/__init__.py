from flask import Flask
import os
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from src.db import db
from src.auth import auth

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(test_config=None): 
    app = Flask(__name__, instance_relative_config=True)

    login_manager.login_view = "auth.login"

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            )
    else:
        app.config.from_mapping(test_config)

            
    db.app=app
    db.init_app(app)    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(auth)
    
    return app