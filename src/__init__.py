from flask import Flask
import os
from flask_smorest import Api


def create_app(test_config=None): 
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:

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
        
    api = Api(app)

    from src.main import llm_blp

    api.register_blueprint(llm_blp)

    return app