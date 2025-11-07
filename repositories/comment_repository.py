from models import Comment

from repositories.base_repository import BaseRepository

class CommentRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_by_id(self, id):
        return Comment.query.get(id)
    
    def get_all(self, post_id):
        return Comment.query.filter_by(
            post_id = post_id,
            is_visible = True
        ).order_by(Comment.created_at.asc()).all()
