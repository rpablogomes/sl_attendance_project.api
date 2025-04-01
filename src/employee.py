from flask import Blueprint, request, jsonify
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.employee import Employee
from src.schemas.create import CreateSchema
from src.schemas.login import LoginSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST,HTTP_200_OK

employee = Blueprint("employee", __name__, url_prefix="/api/v1/employee")

create_schema = CreateSchema()
login_schema = LoginSchema()

@employee.post("/register")
def register():
    
    errors = create_schema.validate(request.json)
    if errors:
        return jsonify(errors), HTTP_400_BAD_REQUEST
    
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    family_name = request.json.get("family_name")

    employee = Employee.query.filter_by(email=email).first()

    if employee:
        return jsonify({"message": "Email already exists"}), HTTP_400_BAD_REQUEST

    password_hash = Employee.set_password(password)

    print(type(password_hash))

    employee = Employee(
        email=email, 
        password_hash=password_hash,
        name=name,
        family_name=family_name
        )
    
    employee.save()

    return jsonify(employee.dict()), 201

logging.basicConfig(level=logging.DEBUG)

@employee.get("/me")
@jwt_required()
def get_employee():
    employee = Employee.query.filter_by(id=14).first()

    return jsonify(employee.dict()), HTTP_200_OK

    # return "ok", 200