from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView

from services.post_service import PostService
from services.user_service import UserService

from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from functools import wraps
from models import User, UserCredential, Post, Comment, Category
from schemas import UserSchema, RegisterSchema, PostSchema, LoginSchema, CommentSchema, CategorySchema
    
def role_required(*allowes_roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get('role')
            if not role or role not in allowes_roles:
                return {"Error": "Access denied for this role."}
            return fn(*args, **kwargs)
        return wrapper
    return decorator

class UserPosts(MethodView):
    def __init__(self):
        self.service = PostService()

    def get(self):
        posts = self.service.get_all_posts()
        return PostSchema(many=True).dump(posts), 200
    
    @jwt_required()
    def post(self):
        try:
            post = self.service.create_post(request.json, get_jwt_identity())
            return PostSchema().dump(post), 201
        except ValidationError as e:
            return {"Errors": e.messages}, 400
        
    @jwt_required()
    def put(self, id):
        try:
            post = self.service.update_post(id, request.json, int(get_jwt_identity()))
            return PostSchema().dump(post), 200
        except ValidationError as e:
            return {"Error": e.messages}, 400

    @jwt_required()
    def patch(self, id):
        try:
            post = self.service.patch_post(id, request.json, int(get_jwt_identity()))
            return PostSchema().dump(post), 200
        except PermissionError as e:
            return {"Error": str(e)}, 403
        except ValidationError as e:
            return {"Error": e.messages}, 400
    
    @jwt_required()
    def delete(self, id):
        try:
            self.service.delete_post(id, int(get_jwt_identity()))
            return '', 204
        except PermissionError as e:
            return {"Error": str(e)}, 403


class UserAPI(MethodView):
    def __init__(self):
        self.service = UserService()

    def get(self):
        users = self.service.get_all_users()
        return UserSchema(many=True).dump(users)

class UserDetailAPI(MethodView):
    def __init__(self):
        self.service = UserService()

    @jwt_required()
    def get(self, id):
        user = self.service.get_user_by_id(id)
        return UserSchema().dump(user), 200
    
    @role_required("admin")
    def put(self, id):
        try:
            data = UserSchema().load(request.json)
            user = self.service.update_user(id, data)
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}, 400
        except ValueError as e:
            return {"Error": str(e)}, 400

    @role_required("admin")
    def patch(self, id):
        try:
            data = UserSchema(partial=True).load(request.json)
            user = self.service.patch_user(id, data)
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}, 400
        except ValueError as e:
            return {"Error": str(e)}, 400
    
    @role_required("admin")
    def delete(self, id):
        try:
            self.service.delete_user(id)
            return {"Message": "User deleted."}, 204
        except ValueError as e:
            return {"Error": str(e)}, 400

class UserRegisterAPI(MethodView):
    def __init__(self):
        self.service = UserService()

    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as e:
            return {"Error": e.messages}, 400
        
        try:
            new_user = self.service.register_user(data)
        except ValueError as e:
            return {"Error": str(e)}, 400
        return UserSchema().dump(new_user), 201
    
class LoginAPI(MethodView):
    def __init__(self):
        self.service = UserService()

    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as e:
            return {"Error": e.messages}, 400
        
        try:
            token = self.service.user_login(data)
            return jsonify(access_token = token), 200
        except ValidationError as e:
            return {"Error": e.messages}, 400