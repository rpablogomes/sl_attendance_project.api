from flask import Blueprint
# from flask_marshmallow import Marshmallow

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post("/register")
def register():
    return "User created"

@auth.post("/me")
def teste():
    return "me"

