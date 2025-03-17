from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from marshmallow import ValidationError
from src.models.employee import Employee
from src.schemas.login import LoginSchema

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
login_schema = LoginSchema()

@auth.post("/login")
def login():
    data = request.get_json()

    try:
        validated_data = login_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


    employee = Employee.query.filter_by(email=validated_data["email"]).first()
    if employee and employee.check_password(validated_data["password"]):
        login_user(employee)
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@auth.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200
