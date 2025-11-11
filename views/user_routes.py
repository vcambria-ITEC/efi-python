from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas import UserSchema
from services.user_service import UserService
from utils.decorators import role_required

blp = Blueprint("Users", "users", url_prefix="/api/users")

# ------------ USER LIST (admin only) ------------
@blp.route("/")
class UserListResource(MethodView):
    def __init__(self):
        self.service = UserService()

    @jwt_required()
    @role_required("admin")
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = self.service.get_all_users()
        return users


# ------------ USER DETAIL ------------
@blp.route("/<int:id>")
class UserDetailResource(MethodView):
    def __init__(self):
        self.service = UserService()

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, id):
        current_user_id = int(get_jwt_identity())
        user = self.service.get_user_detail_by_id(id, current_user_id)
        return user

    @jwt_required()
    @role_required("admin")
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, data, id):
        user = self.service.update_user(id, data)
        return user

    @jwt_required()
    @role_required("admin")
    @blp.arguments(UserSchema(partial=True))
    @blp.response(200, UserSchema)
    def patch(self, data, id):
        user = self.service.patch_user(id, data)
        return user

    @jwt_required()
    @role_required("admin")
    @blp.response(204)
    def delete(self, id):
        self.service.delete_user(id)
        return ""