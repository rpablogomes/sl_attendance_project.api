from flask import Flask
import os
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_smorest import Api
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
        app.config["API_TITLE"] = "My API"
        app.config["API_VERSION"] = "v1"
        app.config["OPENAPI_VERSION"] = "3.0.2"
        app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_REDOC_PATH"] = "/redoc"
        app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
        app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        app.config["OPENAPI_RAPIDOC_PATH"] = "/rapidoc"
        app.config["OPENAPI_RAPIDOC_URL"] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    else:
        app.config.from_mapping(test_config)

    from src.database.db import db, init_db

    init_db(app)
    Migrate(app, db)
    Marshmallow(app)
    JWTManager(app)

    from src.auth import auth
    from src.employee import employee

    api = Api(app)
    api.register_blueprint(auth)
    api.register_blueprint(employee)

    # Register models
    from src.models.employee import Employee
    from src.models.leave_request import LeaveRequest
    from src.models.attedance import Attendance

    return app