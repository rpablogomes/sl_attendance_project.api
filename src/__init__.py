from flask import Flask
import os
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restx import Api

from src.db import db, init_db

bcrypt = Bcrypt()

def create_app(test_config=None): 
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config["DEBUG"] = True 
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'JWT_SECRET_KEY')
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
        )
    else:
        app.config.from_mapping(test_config)

    api = Api(app, title="Bookmarks API", version="1.0", description="Employee Management API")
    init_db(app)
    Migrate(app, db)
    Marshmallow(app)
    JWTManager(app)
    
    from src.auth import auth, auth_ns
    from src.employee import employee, employee_ns

    # Register blueprints / routes
    app.register_blueprint(auth)
    app.register_blueprint(employee)

    # swagger
    
    api.add_namespace(employee_ns)
    api.add_namespace(auth_ns)

    # Register models
    from src.models.employee import Employee
    from src.models.leave_request import LeaveRequest
    from src.models.attedance import Attendance

    return app