from app import db
from marshmallow import Schema, fields, validate
from models import User, Post, Comment, Category

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(load_only=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class UserCredentialSchema(Schema):
    id = fields.Int(dump_only=True)
    role = fields.Str(required=True)
    user_id = fields.Int(required=True)
    user = fields.Nested("UserSchema", only=("id", "username", "email"), dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(attribute="credential.role", dump_only=True)

    posts = fields.List(
        fields.Nested("PostSchema", exclude=("author",)),
        dump_only=True
    )
    comments = fields.List(
        fields.Nested("CommentSchema", exclude=("author",)),
        dump_only=True
    )

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))   

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    created_at = fields.DateTime(dump_only=True)
    is_visible = fields.Bool(dump_only=True)

    author = fields.Nested(
        "UserSchema",
        only=("id", "username"),
        dump_only=True
    )

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    content = fields.Str(required=True, validate=validate.Length(min=5, max=500))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_published = fields.Bool(dump_only=True)
    category_ids = fields.List(fields.Int(), load_only=True)

    author = fields.Nested(
        "UserSchema",
        only=("id", "username"),
        dump_only=True
    )

    comments = fields.List(
        fields.Nested("CommentSchema"),
        dump_only=True
    )

    categories = fields.List(
        fields.Nested("CategorySchema"),
        dump_only=True
    )
