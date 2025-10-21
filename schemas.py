from marshmallow import Schema, fields

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

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    
    author = fields.Nested(
        "UserSchema", 
        only=("id", "username"), 
        dump_only=True
    )

class PostSchema(Schema):

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
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
