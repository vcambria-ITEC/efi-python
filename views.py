from datetime import timedelta
from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView
from flask_login import current_user

from services.post_service import PostService
from services.user_service import UserService

from passlib.hash import bcrypt
from flask_jwt_extended import (  #pip install Flask-JWT-Extended
    jwt_required,
    create_access_token,
    get_jwt,
    get_jwt_identity
)
from functools import wraps
from typing import Any, Dict
from app import db
from models import User, UserCredential, Post, Comment, Category
from schemas import UserSchema, RegisterSchema, PostSchema, LoginSchema, CommentSchema, CategorySchema

def is_propietary(proptierary_id, current_id):
    return proptierary_id == current_id  
    
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
            return PostSchema().dump(new_post), 201
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
        users = User.query.all()
        return UserSchema(many=True).dump(users)

    def post(self):
        try:
            data = UserSchema().load(request.json)
            new_user = User(
                name=data.get('name'),
                email=data.get('email')
            )
            db.session.add(new_user)
            db.session.commit()
        except ValidationError as err:
            return {"Errors": f"{err.messages}"}, 400
        return UserSchema().dump(new_user), 201

class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, id):
        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200
    
    @role_required("admin")
    def put(self, id):
        user = User.query.get_or_404(id)
        try: 
            data = UserSchema().load(request.json)
            user.name = data['username']
            user.email = data['email']
            db.session.commit()
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}

    @role_required("admin")
    def patch(self, id):
        user = User.query.get_or_404(id)
        try: 
            data = UserSchema(partial=True).load(request.json)
            if 'username' in data:
                user.username = data.get('username')
            if 'email' in data:
                user.email = data.get('email')
            db.session.commit()
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}
    
    @role_required("admin")
    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"Message": "Deleted User"}, 204
        except:
            return {"Error": "No es posible borrarlo"}

class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"Error": err.messages}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"Error": "Email en uso"}), 400
        
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.flush()
        
        password_hash = bcrypt.hash(data['password'])
        credenciales = UserCredential(
            user_id=new_user.id, 
            password_hash=password_hash,
            role=data['role']
        )  
        db.session.add(credenciales)
        db.session.commit()
        return UserSchema().dump(new_user)
    
class LoginAPI(MethodView):
    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {"Error": err.messages}
        
        user = User.query.filter_by(username=data["username"]).first()

        if not user or not user.credential:
            return {"error": "no posee credenciales"}, 404
        
        if not bcrypt.verify(data["password"], user.credential.password_hash):
            return {"error": "Credenciales invalidas"}, 400

        additional_claims = {
            "email": user.email,
            "role": user.credential.role,
            "username": user.username
        }
        identity = str(user.id)
        token = create_access_token(
            identity=identity, 
            additional_claims=additional_claims, 
            expires_delta=timedelta(minutes=30)
        )

        return jsonify(access_token=token)