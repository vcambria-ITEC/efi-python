from datetime import timedelta
from repositories.user_repository import UserRepository
from models import User, UserCredential
from passlib.hash import bcrypt
from utils.check_role import is_owner
from utils.message_utils import USER_DETAIL_PERMISSION_ERROR
from flask_jwt_extended import create_access_token

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_all_users(self):
        return self.repo.get_all()
    
    def get_user_by_id(self, id):
        return self.repo.get_by_id(id)
    
    def get_user_detail_by_id(self, id, current_user_id):
        if not is_owner(current_user_id, id):
            raise PermissionError(USER_DETAIL_PERMISSION_ERROR)
        return self.get_user_by_id(id)

    def user_login(self, data):
        username = data['username']

        user = self.repo.get_by_username(username)
        if not user or not user.credential:
            raise ValueError("User not found.")

        if not user.is_active:
            raise ValueError("User inactive.")

        if not bcrypt.verify(data["password"], user.credential.password_hash):
            raise ValueError("User not found.")
        
        additional_claims = {
            "email": user.email,
            "role": user.credential.role,
            "user_id": user.id
        }
        identity = str(user.id)
        token = create_access_token(
            identity=identity, 
            additional_claims=additional_claims, 
            expires_delta=timedelta(hours=24)
        )

        return token

    def register_user(self, data):
        username= data['username']
        email= data['email']
        password= data['password']
        role = data.get('role', 'user')

        if self.repo.get_by_email(email):
            raise ValueError("Email already in use.")
        
        try:
            new_user = User(username=username, email=email)
            self.repo.save(new_user)

            self.repo.flush()
            password_hash = bcrypt.hash(password)

            credentials = UserCredential(
                user_id = new_user.id,
                password_hash = password_hash,
                role = role
            )

            self.repo.save(credentials)
            self.repo.commit()
            return new_user
        except Exception as e:
            self.repo.rollback()
            raise ValueError(f"Error during registration: {str(e)}")
    
    def update_user(self, id, data):
        user = self.get_user_by_id(id)

        if data['email'] != user.email and self.repo.get_by_email(data['email']):
            raise ValueError("Email already in use.")
        
        user.username = data['username']
        user.email = data['email']
        
        try:
            self.repo.commit()
            return user
        except Exception as e:
            self.repo.rollback()
            raise ValueError(f"Error updating user: {str(e)}")
        
    def patch_user(self, id, data):
        user = self.get_user_by_id(id)

        if 'email' in data and data['email'] != user.email:
            if self.repo.get_by_email(data['email']):
                raise ValueError("Email already in use.")
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        try:
            self.repo.commit()
            return user
        except Exception as e:
            raise ValueError(f"Error patching user: {str(e)}")

    def delete_user(self, id):
        user = self.get_user_by_id(id)

        try:
            if user.credential:
                user.credential.is_active = False
            user.is_active = False
            self.repo.commit()
        except Exception as e:
            self.repo.rollback()
            raise ValueError(f"Error deleting user, it may be in use: {str(e)}")