from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from src.models.employee import Employee
from src.schemas.employee.register import RegisterSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST,HTTP_200_OK

employee_blp = Blueprint("employee", __name__, url_prefix="/api/v1/employee", description="Employee Management Endpoints")

@employee_blp.route("/register")
class Register(MethodView):
    @employee_blp.arguments(RegisterSchema)
    def post(self, args):
        """Create a employee"""
        email = args.get("email")
        password = args.get("password")
        name = args.get("name")
        family_name = args.get("family_name")

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
        
        return jsonify({
            "message": "Employee created successfully",
            **employee.dict()
        }), HTTP_200_OK

@employee_blp.route("/me")
@employee_blp.response(200, RegisterSchema())
@employee_blp.response(400, RegisterSchema())
class Me(MethodView):
    @jwt_required()
    def get(self):
        """Return data of employee"""
        user_id = get_jwt_identity()
        employee = Employee.query.filter_by(id=user_id).first()

        return jsonify(employee.dict()), HTTP_200_OK
