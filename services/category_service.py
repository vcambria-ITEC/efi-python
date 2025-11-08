from models import Category
from repositories.category_repository import CategoryRepository
from utils.exception_utils import NotFoundError, ConflictError
from utils.message_utils import CATEGORY_NOT_FOUND

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all_categories(self):
        categories = self.repo.get_all_categories()
        if not categories:
            raise NotFoundError('No categories exist in database.')
        return categories

    def get_category_by_id(self, category_id):
        category = self.repo.get_category_by_id(category_id)
        if not category:
            raise NotFoundError(CATEGORY_NOT_FOUND)

    def create_category(self, data):

        categories = self.repo.get_all_categories()

        for category in categories:
            if data['name'] == category.name:
                raise ConflictError("The category name already exists.")

        category = Category(
            name = data['name']
        )
        self.repo.save(category)
        self.repo.commit()
        return category

    def update_category(self, category_id, data):
        category = self.repo.get_category_by_id(category_id)

        if not category:
            raise NotFoundError(CATEGORY_NOT_FOUND)

        category.name = data.get('name', category.name)
        self.repo.commit()
        return category
    
    def delete_category(self, category_id):
        category = self.repo.get_category_by_id(category_id)

        if not category:
            raise NotFoundError(CATEGORY_NOT_FOUND)

        category.is_active = False
        self.repo.commit()
        return True