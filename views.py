from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView
from services.post_service import PostService
from services.user_service import UserService
from services.comment_service import CommentService
from services.stats_service import StatsService
from services.category_service import CategoryService
from utils.exception_utils import UpdateError, DeleteError

from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from functools import wraps
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

class UserPostsAPI(MethodView):
    def __init__(self):
        self.service = PostService()

    def get(self):
        posts = self.service.get_all_posts()
        return PostSchema(many=True).dump(posts), 200

class UserPostDetailAPI(MethodView):
    def __init__(self):
        self.service = PostService()
    
    def get(self, id):
        post = self.service.get_post_by_id(id)
        return PostSchema().dump(post), 200
    
    @jwt_required()
    def post(self):
        post = self.service.create_post(request.json, get_jwt_identity())
        return PostSchema().dump(post), 201
        
    @jwt_required()
    def put(self, id):
        post = self.service.update_post(id, request.json, int(get_jwt_identity()))
        return PostSchema().dump(post), 200

    @jwt_required()
    def patch(self, id):
        post = self.service.patch_post(id, request.json, int(get_jwt_identity()))
        return PostSchema().dump(post), 200
    
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

    @jwt_required()
    @role_required("admin")
    def get(self):
        users = self.service.get_all_users()
        return UserSchema(many=True).dump(users)

class UserDetailAPI(MethodView):
    def __init__(self):
        self.service = UserService()

    @jwt_required()
    def get(self, id):
        current_user_id = int(get_jwt_identity())
        user = self.service.get_user_detail_by_id(id, current_user_id)
        return UserSchema().dump(user), 200
    
    @jwt_required()
    @role_required("admin")
    def put(self, id):
        try:
            data = UserSchema().load(request.json)
            user = self.service.update_user(id, data)
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}, 400
        except UpdateError as e:
            return {"Error": str(e)}, 400

    @jwt_required()
    @role_required("admin")
    def patch(self, id):
        try:
            data = UserSchema(partial=True).load(request.json)
            user = self.service.patch_user(id, data)
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}, 400
        except UpdateError as e:
            return {"Error": str(e)}, 400
    
    @jwt_required()
    @role_required("admin")
    def delete(self, id):
        try:
            self.service.delete_user(id)
            return {"Message": "User deleted."}, 204
        except DeleteError as e:
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
        

class PostCommentAPI(MethodView):

    def __init__(self):
        self.service = CommentService()

    def get(self, post_id):
        comments = self.service.get_comments_for_post(post_id)
        return CommentSchema(many=True).dump(comments), 200
    
    @jwt_required()
    def post(self, post_id):
        data = CommentSchema().load(request.json)
        author_id = int(get_jwt_identity())
        new_comment = self.service.create_comment(data, author_id, post_id)

        return CommentSchema().dump(new_comment), 201

class CommentAPI(MethodView):
    def __init__(self):
        self.service = CommentService()

    @jwt_required()
    def delete(self, comment_id):
        current_user_id = int(get_jwt_identity())
        self.service.delete_comment(comment_id, current_user_id)
        return '', 204
    
    @jwt_required()
    def patch(self, comment_id):
        data = CommentSchema().load(request.json)
        author_id = int(get_jwt_identity())
        comment = self.service.update_comment(comment_id, data, author_id)
        return CommentSchema().dump(comment), 200

class CategoriesAPI(MethodView):
    def __init__(self):
        self.service = CategoryService()
    
    def get(self):
        categories = self.service.get_all_categories()
        return CategorySchema(many=True).dump(categories), 200
    
    @jwt_required()
    @role_required("admin", "moderator")
    def post(self):
        data = CategorySchema().load(request.json)
        new_category = self.service.create_category(data)
        return CategorySchema().dump(new_category), 201

class CategoryAPI(MethodView):
    def __init__(self):
        self.service = CategoryService()
    
    @jwt_required()
    def get(self, category_id):
        category = self.service.get_category_by_id(category_id)
        return CategorySchema(many=False).dump(category), 200
    
    @role_required("admin", "moderator")
    def put(self, category_id):
        data = CategorySchema().load(request.json)
        category = self.service.update_category(category_id, data)
        return CategorySchema().dump(category), 200
    
    @role_required("admin")    
    def delete(self, category_id):
        self.service.delete_category(category_id)
        return '', 204
        
class StatsAPI(MethodView):

    def __init__(self):
        self.service = StatsService()

    @jwt_required()
    @role_required("admin", "moderator")
    def get(self):
        current_role = get_jwt().get('role')
        stats = self.service.get_stats(current_role)
        return jsonify(stats), 200