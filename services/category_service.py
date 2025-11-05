from models import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all_categories(self):
        return self.repo.get_all_categories()

    def get_category_by_id(self, category_id):
        return self.repo.get_category_by_id(category_id)
    
    def create_category(self, data):
        category = Category(
            name = data['name']
        )
        self.repo.save(category)
        self.repo.commit()
        return category

    def update_category(self, category_id, data):
        category = self.repo.get_category_by_id(category_id)
        category.name = data.get('name', category.name)
        self.repo.commit()
        return category
    
    def delete_category(self, category_id):
        category = self.repo.get_category_by_id(category_id)
        category.is_active = False
        self.repo.commit()
        return True