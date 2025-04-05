from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_smorest import Blueprint

from src.models.employee import Employee
from src.schemas.auth.login import LoginSchema
from src.static.http_status_code import HTTP_400_BAD_REQUEST ,HTTP_200_OK

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.route("/login")
class Login(MethodView):
    @auth.arguments(LoginSchema)
    @auth.response(HTTP_200_OK, LoginSchema)
    def post(self, args):
        email = args.get("email")
        password = args.get("password")

        employee = Employee.query.filter_by(email=email).first()

        if employee and Employee.check_password(password, employee.password_hash):
            refresh = create_refresh_token(identity=employee.id)
            access = create_access_token(identity=employee.id)

            return jsonify({
                "refresh": refresh,
                "access": access,
                **employee.dict()
            }), HTTP_200_OK

        return jsonify({"message": "Invalid credentials"}), HTTP_400_BAD_REQUEST

@auth.route("/logout")
class Logout(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        return jsonify({"message": "Logged out"}), HTTP_200_OK

@auth.route("/token/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access = create_access_token(identity=identity)
        return jsonify({"access": access}), HTTP_200_OK
