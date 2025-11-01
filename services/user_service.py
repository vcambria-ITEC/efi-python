from repositories.user_repository import UserRepository
from models import User, UserCredential
from marshmallow import ValidationError
from schemas import UserSchema

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_all_users(self):
        return self.repo.get_all()
        
