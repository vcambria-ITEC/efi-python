from repositories.comment_repository import CommentRepository
from repositories.post_repository import PostRepository
from models import Comment
from marshmallow import ValidationError
from schemas import CommentSchema


class CommentService:
    ERROR_NOT_OWNER = "No eres el propietario de este comentario."
    ERROR_NOT_MODERATOR = "No tienes permisos para esta acción."
    ERROR_POST_NOT_FOUND = "El post no existe."


    def __init__(self):
        self.repo = CommentRepository()
        self.post_repo = PostRepository

    
    def get_comments_for_post(self, post_id):

        try:
            self.post_repo.get_by_id(post_id)
        except:
            raise ValueError(self.ERROR_POST_NOT_FOUND)
        
        return self.repo.get_all_for_post(post_id)
    

    def create_comment(self,data, author_id, post_id):

        try:
            dto = CommentSchema().load(data)
        except ValidationError as e:
            raise e
        
        try:
            self.post_repo.get_by_id(post_id)
        except Exception:
            raise ValueError(self.ERROR_POST_NOT_FOUND)
        

        comment = Comment(
            content = dto['content'],
            user_id = author_id,
            post_id = post_id
        )

        self.repo.save(comment)
        return comment
    
    def update_comment(self, comment_id, data, current_user_id):

        comment = self.repo.get_by_id(comment_id)

        if comment.user_id != current_user_id:
            raise PermissionError(self.ERROR_NOT_OWNER)
        
        try:
            dto = CommentSchema(partial=True).load(data)
        except ValidationError as e:
            raise e
        
        comment.content = dto.get('content', comment.content)

        self.repo.update()
        return comment


    def delete_comment(self, comment_id):

        comment = self.repo.get_by_id(comment_id)

        comment.is_visible = False

        self.repo.update()

        return True