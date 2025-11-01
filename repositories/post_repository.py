from models import Post, Category, db
from base_repository import BaseRepository

class PostRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return Post.query.filter_by(is_published=True).all()

    def get_by_id(self, id):
        return Post.query.get_or_404(id)
