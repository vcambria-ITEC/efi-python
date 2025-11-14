from repositories.comment_repository import CommentRepository
from services.post_service import PostService
from models import Comment
from utils.message_utils import (
    COMMENT_OWNERSHIP_ERROR,
    POST_NOT_FOUND_ERROR,
    COMMENT_NOT_FOUND_ERROR
)
from utils.check_role import is_owner, get_role
from utils.exception_utils import (
    NotFoundError,
    ForbiddenError
)

class CommentService:

    def __init__(self):
        self.repo = CommentRepository()
        self.post_service = PostService()

    def get_comments_for_post(self, post_id):
        return self.repo.get_all(post_id)
    
    def create_comment(self, data, author_id, post_id):
        post = self.post_service.get_post_by_id(post_id)
        if not post:
            raise NotFoundError(POST_NOT_FOUND_ERROR)

        comment = Comment(
            content = data['content'],
            user_id = author_id,
            post_id = post_id
        )

        self.repo.save(comment)
        self.repo.commit()
        return comment
    
    def update_comment(self, comment_id, data, current_user_id):

        comment = self.repo.get_by_id(comment_id)

        if not comment:
            raise NotFoundError(COMMENT_NOT_FOUND_ERROR)

        if not is_owner(current_user_id, comment.user_id):
            raise ForbiddenError(COMMENT_OWNERSHIP_ERROR)
        
        comment.content = data.get('content', comment.content)

        self.repo.commit()
        return comment


    def delete_comment(self, comment_id, current_user_id):

        comment = self.repo.get_by_id(comment_id)

        if not comment:
            raise NotFoundError(COMMENT_NOT_FOUND_ERROR)
        
        if not is_owner(current_user_id, comment.user_id) and get_role() != 'moderator':
            raise ForbiddenError(COMMENT_OWNERSHIP_ERROR)

        comment.is_visible = False

        self.repo.commit()

        return True
