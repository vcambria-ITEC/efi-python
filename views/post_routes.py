from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import PostSchema
from services.post_service import PostService

blp = Blueprint("Posts", "posts", url_prefix="/api/posts")

@blp.route("/")
class PostListResource(MethodView):
    def __init__(self):
        self.service = PostService()

    @blp.doc(security=[])
    @blp.response(200, PostSchema(many=True))
    def get(self):
        posts = self.service.get_all_posts()
        return posts

    @jwt_required()
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, data):
        post = self.service.create_post(data, int(get_jwt_identity()))
        return post


@blp.route("/<int:id>")
class PostDetailResource(MethodView):
    def __init__(self):
        self.service = PostService()

    @blp.doc(security=[])
    @blp.response(200, PostSchema)
    def get(self, id):
        post = self.service.get_post_by_id(id)
        return post

    @jwt_required()
    @blp.arguments(PostSchema)
    @blp.response(200, PostSchema)
    def put(self, data, id):
        post = self.service.update_post(id, data, int(get_jwt_identity()))
        return post

    @jwt_required()
    @blp.arguments(PostSchema(partial=True))
    @blp.response(200, PostSchema)
    def patch(self, data, id):
        post = self.service.patch_post(id, data, int(get_jwt_identity()))
        return post

    @jwt_required()
    @blp.response(204)
    def delete(self, id):
        self.service.delete_post(id, int(get_jwt_identity()))
        return ""
