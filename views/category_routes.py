from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from schemas import CategorySchema
from services.category_service import CategoryService
from utils.decorators import role_required

blp = Blueprint("Categories", "categories", url_prefix="/api/categories")

@blp.route("/")
class CategoryListResource(MethodView):
    def __init__(self):
        self.service = CategoryService()

    @blp.doc(security=[])
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        categories = self.service.get_all_categories()
        return categories

    @jwt_required()
    @role_required("admin", "moderator")
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, data):
        new_category = self.service.create_category(data)
        return new_category


@blp.route("/<int:category_id>")
class CategoryResource(MethodView):
    def __init__(self):
        self.service = CategoryService()

    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = self.service.get_category_by_id(category_id)
        return category

    @jwt_required()
    @role_required("admin", "moderator")
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def put(self, data, category_id):
        category = self.service.update_category(category_id, data)
        return category

    @jwt_required()
    @role_required("admin")
    @blp.response(204)
    def delete(self, category_id):
        self.service.delete_category(category_id)
        return ""
