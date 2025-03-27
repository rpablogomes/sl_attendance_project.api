from flask import Flask
import os
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

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
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
            )
    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    ma = Marshmallow(app)

    JWTManager(app)
    
    app.register_blueprint(auth)

    from src.models.employee import Employee
    from src.models.leave_request import LeaveRequest
    from src.models.attedance import Attendance

    return app