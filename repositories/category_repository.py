from models import Category

from repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_all_categories(self):
        return Category.query.filter_by(is_active=True).all()
    
    def get_category_by_id(self, id):
        return Category.query.get_or_404(id)