from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from schemas import RegisterSchema, UserSchema, LoginSchema
from services.user_service import UserService
from marshmallow import ValidationError

blp = Blueprint("Auth", "auth", url_prefix="/api")

@blp.route("/register")
class UserRegisterResource(MethodView):
    def __init__(self):
        self.service = UserService()
    
    @blp.doc(security=[])
    @blp.arguments(RegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        new_user = self.service.register_user(data)
        return new_user
    
@blp.route("/login")
class LoginResource(MethodView):
    def __init__(self):
        self.service = UserService()

    @blp.doc(security=[])
    @blp.arguments(LoginSchema)
    @blp.response(200)
    def post(self, data):
        token = self.service.user_login(data)
        return {"access_token": token}
