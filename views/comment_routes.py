from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import CommentSchema
from services.comment_service import CommentService

blp = Blueprint("Comments", "comments", url_prefix="/api")

@blp.route("/posts/<int:post_id>/comments")
class PostCommentResource(MethodView):
    def __init__(self):
        self.service = CommentService()

    @blp.doc(security=[])
    @blp.response(200, CommentSchema(many=True))
    def get(self, post_id):
        comments = self.service.get_comments_for_post(post_id)
        return comments

    @jwt_required()
    @blp.arguments(CommentSchema)
    @blp.response(201, CommentSchema)
    def post(self, data, post_id):
        author_id = int(get_jwt_identity())
        new_comment = self.service.create_comment(data, author_id, post_id)
        return new_comment

@blp.route("/comments/<int:comment_id>")
class CommentResource(MethodView):
    def __init__(self):
        self.service = CommentService()

    @jwt_required()
    @blp.response(204)
    def delete(self, comment_id):
        current_user_id = int(get_jwt_identity())
        self.service.delete_comment(comment_id, current_user_id)
        return ""

    @jwt_required()
    @blp.arguments(CommentSchema)
    @blp.response(200, CommentSchema)
    def patch(self, data, comment_id):
        author_id = int(get_jwt_identity())
        comment = self.service.update_comment(comment_id, data, author_id)
        return comment
