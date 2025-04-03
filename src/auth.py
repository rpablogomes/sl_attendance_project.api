from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_restx import Namespace

from src.models.employee import Employee
from src.schemas.create import CreateSchema
from src.schemas.login import LoginSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST, HTTP_200_OK

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
auth_ns = Namespace("auth", description="Authentication related operations")

create_schema = CreateSchema()
login_schema = LoginSchema()

@auth.post("/login")
def login():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications."""
    errors = login_schema.validate(request.json)
    if errors:
        return jsonify(errors), 

    email = request.json.get("email")
    password = request.json.get("password") 

    employee = Employee.query.filter_by(email=email).first()

    if employee:
        is_pass_correct = Employee.check_password(password, employee.password_hash)
        if is_pass_correct:
            refresh = create_refresh_token(identity=employee.id)
            access =  create_access_token(identity=employee.id)

            return jsonify({
                "refresh": refresh,
                "access": access,
                **employee.dict()
            }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), HTTP_400_BAD_REQUEST
                   
@auth.post("/logout")
@jwt_required(refresh=True)
def logout():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications."""
    return jsonify({"message": "Logged out"}), HTTP_200_OK

@auth.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():  
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications."""
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), HTTP_200_OK
    