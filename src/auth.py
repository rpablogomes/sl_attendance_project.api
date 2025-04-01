from flask import Blueprint, request, jsonify
from flask_login import logout_user
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

from src.models.employee import Employee
from src.schemas.create import CreateSchema
from src.schemas.login import LoginSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST, HTTP_200_OK

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

create_schema = CreateSchema()
login_schema = LoginSchema()

@auth.post("/login")
def login():
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
    logout_user()
    return jsonify({"message": "Logged out"}), 200

auth.post("/token/refresh")
@jwt_required()
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), HTTP_200_OK
    