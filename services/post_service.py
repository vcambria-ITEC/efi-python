from repositories.post_repository import PostRepository
from models import Post, Category
from marshmallow import ValidationError
from schemas import PostSchema

class PostService:
    ERROR_NOT_OWNER_MESSAGE = 'You are not the owner of this post.'
    def __init__(self):
        self.repo = PostRepository()

    def get_all_posts(self):
        return self.repo.get_all()

    def create_post(self, data, author_id):
        dto = PostSchema().load(data)

        post = Post(
            title=dto['title'],
            content=dto['content'],
            category_ids=dto['category_ids'],
            author_id=author_id
        )

        self.repo.save(post)
        return post

    def update_post(self, id, data, current_user_id):
        post = self.repo.get_by_id(id)

        if post.author_id != current_user_id:
            raise PermissionError(self.ERROR_NOT_OWNER_MESSAGE)

        dto = PostSchema().load(data)
        post.title = dto['title']
        post.content = dto['content']
        post.category_ids = dto['category_ids']

        self.repo.update()
        return post

    def patch_post(self, id, data, current_user_id):
        post = self.repo.get_by_id(id)

        if post.author_id != current_user_id:
            raise PermissionError(self.ERROR_NOT_OWNER_MESSAGE)

        dto = PostSchema(partial=True).load(data)

        post.title = dto.get('title', post.title)
        post.content = dto.get('content', post.content)

        if 'category_ids' in dto:
            post.categories = Category.query.filter(
                Category.id.in_(dto['category_ids'])
            ).all()

        self.repo.update()
        return post

    def delete_post(self, id, current_user_id):
        post = self.repo.get_by_id(id)
        if post.author_id != current_user_id:
            raise PermissionError(self.ERROR_NOT_OWNER_MESSAGE)
        self.repo.delete(post)
        return True