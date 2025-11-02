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
        
    
