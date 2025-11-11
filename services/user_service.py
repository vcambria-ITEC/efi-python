from datetime import timedelta
from repositories.user_repository import UserRepository
from models import User, UserCredential
from passlib.hash import bcrypt
from utils.exception_utils import AuthError, InactiveUserError, RegisterError, UpdateError, DeleteError, ConflictError, ForbiddenError, NotFoundError
from utils.message_utils import USER_DETAIL_PERMISSION_ERROR, INVALID_CREDENTIALS_ERROR, USED_EMAIL_ERROR, USER_NOT_FOUND
from flask_jwt_extended import create_access_token

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_all_users(self):
        all_users = self.repo.get_all()
        if not all_users:
            raise NotFoundError("No users exist in the database.")
        return all_users

    def get_user_by_id(self, id):
        user = self.repo.get_by_id(id)
        if not user:
            raise NotFoundError(USER_NOT_FOUND)
        return user

    def get_user_detail_by_id(self, id, current_user_id):

        target_user = self.repo.get_by_id(current_user_id)

        if not target_user.is_active:
            raise NotFoundError(USER_NOT_FOUND)

        current_user_role = self.repo.get_by_id(current_user_id).credential.role

        if int(id) != int(current_user_id) and current_user_role != "admin":
            raise ForbiddenError(USER_DETAIL_PERMISSION_ERROR)

        return self.get_user_by_id(id)
    
    def user_login(self, data):
        username = data['username']

        user = self.repo.get_by_username(username)
        if not user or not user.credential:
            raise AuthError(INVALID_CREDENTIALS_ERROR)

        if not user.is_active:
            raise InactiveUserError("User inactive.")

        if not bcrypt.verify(data["password"], user.credential.password_hash):
            raise AuthError(INVALID_CREDENTIALS_ERROR)
        
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
            raise ConflictError(USED_EMAIL_ERROR)
        
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
            raise RegisterError(f"Error during registration: {str(e)}")
    
    def update_user(self, id, data):
        user = self.get_user_by_id(id)
        
        if not user:
            raise NotFoundError(USER_NOT_FOUND)

        if data['email'] != user.email and self.repo.get_by_email(data['email']):
            raise ConflictError(USED_EMAIL_ERROR)
        
        user.username = data['username']
        user.email = data['email']
        
        try:
            self.repo.commit()
            return user
        except Exception as e:
            self.repo.rollback()
            raise UpdateError(f"Error updating user: {str(e)}")
        
    def patch_user(self, id, data):
        user = self.get_user_by_id(id)

        if not user:
            raise NotFoundError(USER_NOT_FOUND)

        if 'email' in data and data['email'] != user.email:
            if self.repo.get_by_email(data['email']):
                raise ConflictError(USED_EMAIL_ERROR)
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        try:
            self.repo.commit()
            return user
        except Exception as e:
            raise UpdateError(f"Error patching user: {str(e)}")

    def delete_user(self, id):
        user = self.get_user_by_id(id)

        if not user:
            raise NotFoundError(USER_NOT_FOUND)

        try:
            if user.credential:
                user.credential.is_active = False
            user.is_active = False
            self.repo.commit()
        except Exception as e:
            self.repo.rollback()
            raise DeleteError(f"Error deleting user, it may be in use: {str(e)}")