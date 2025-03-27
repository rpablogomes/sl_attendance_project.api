from flask import Blueprint, request, jsonify
from flask_login import logout_user, login_required
from werkzeug.security import check_password_hash, ∂
from flask_jwt_extended import create_refresh_token

from src.models.employee import Employee
from src.schemas.create import CreateSchema
from src.schemas.login import LoginSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST

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
        is_pass_correct = check_password_hash(employee.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=employee.id)
            access =  create_refresh_token(identity=employee.id)

            return jsonify({
                "refresh": refresh,
                "access": access,
                **employee.dict()
            }), 200

    else:
        return jsonify({"message": "Invalid credentials"}), HTTP_400_BAD_REQUEST
                  
@auth.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200