from repositories.post_repository import PostRepository
from models import Post, Category
from schemas import PostSchema
from utils.check_role import is_owner

from utils.message_utils import (
    POST_OWNERSHIP_ERROR,
    POST_NOT_FOUND_ERROR,
)

from utils.exception_utils import (
    ForbiddenError,
    NotFoundError,
    ConflictError
)

class PostService:
    def __init__(self):
        self.repo = PostRepository()

    def get_all_posts(self):
        posts = self.repo.get_all()

        if not posts:
            raise NotFoundError('No posts available yet')

        return posts

    def get_post_by_id(self, post_id):
        target_post = self.repo.get_by_id(post_id)

        if not target_post:
            raise NotFoundError(POST_NOT_FOUND_ERROR)

        if not target_post.is_published:
            raise NotFoundError(POST_NOT_FOUND_ERROR)
        return target_post

    def create_post(self, data, author_id):
        dto = PostSchema().load(data)
        post = Post(
            title=dto['title'],
            content=dto['content'],
            author_id=author_id
        )

        category_ids = dto.get('category_ids', [])

        if len(category_ids) != len(set(category_ids)):
            raise ConflictError("Duplicate category IDs are not allowed.")

        if category_ids:
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            
            found_ids = {cat.id for cat in categories}
            missing_ids = set(category_ids) - found_ids

            if missing_ids:
                raise NotFoundError(f"The following category IDs do not exist:{list(missing_ids)}")
            
            post.categories = categories

        self.repo.save(post)
        self.repo.commit()
        return post

    def update_post(self, id, data, current_user_id):
        post = self.repo.get_by_id(id)

        if not post:
            raise NotFoundError(POST_NOT_FOUND_ERROR)

        if not is_owner(current_user_id, post.author_id):
            raise ForbiddenError(POST_OWNERSHIP_ERROR)

        dto = PostSchema().load(data)
        post.title = dto['title']
        post.content = dto['content']
        post.category_ids = dto['category_ids']

        self.repo.commit()
        return post

    def patch_post(self, id, data, current_user_id):
        post = self.repo.get_by_id(id)

        if not post:
            raise NotFoundError(POST_NOT_FOUND_ERROR)

        if not is_owner(current_user_id, post.author_id):
            raise ForbiddenError(POST_OWNERSHIP_ERROR)

        dto = PostSchema(partial=True).load(data)

        post.title = dto.get('title', post.title)
        post.content = dto.get('content', post.content)
        post.category_ids = dto.get('category_ids', post.category_ids)

        if 'category_ids' in dto:
            post.categories = Category.query.filter(
                Category.id.in_(dto['category_ids'])
            ).all()

        self.repo.commit()
        return post

    def delete_post(self, id, current_user_id):
        post = self.repo.get_by_id(id)

        if not post:
            raise NotFoundError(POST_NOT_FOUND_ERROR)

        if not is_owner(current_user_id, post.author_id):
            raise ForbiddenError(POST_OWNERSHIP_ERROR)
            
        post.is_published = False
        self.repo.commit()
        return True