from flask import request, jsonify
from flask.views import MethodView
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from src.models.employee import Employee
from src.schemas.employee.register import RegisterSchema
from src.schemas.auth.login import LoginSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST,HTTP_200_OK

employee = Blueprint("employee", __name__, url_prefix="/api/v1/employee", description="Employee Management Endpoints")

login_schema = LoginSchema()

@employee.route("/register")
@employee.arguments(RegisterSchema, location="query")
@employee.response(200, RegisterSchema())
@employee.response(400, RegisterSchema())
class Register(MethodView):
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")
        name = request.json.get("name")
        family_name = request.json.get("family_name")

        employee = Employee.query.filter_by(email=email).first()

        if employee:
            return jsonify({"message": "Email already exists"}), HTTP_400_BAD_REQUEST

        password_hash = Employee.set_password(password)

        employee = Employee(
            email=email, 
            password_hash=password_hash,
            name=name,
            family_name=family_name
            )
        
        employee.save()

@employee.route("/me")
class Employee(MethodView):
    @jwt_required()
    def get(self):
        """Example endpoint returning a list of colors by palette
        This is using docstrings for specifications."""
        user_id = get_jwt_identity()
        print(user_id)
        employee = Employee.query.filter_by(id=user_id).first()

        return jsonify(employee.dict()), HTTP_200_OK
