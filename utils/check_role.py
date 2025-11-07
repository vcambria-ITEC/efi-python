from services.user_service import UserService

from flask_jwt_extended import get_jwt

userService = UserService()

def is_owner(current_user_id, resource_owner_id):
    # current_user = userService.get_user_by_id(current_user_id)
    claims = get_jwt()
    if claims['role'] == 'admin':
        return True
    return current_user_id == resource_owner_id

def get_role():
    return get_jwt().get('role')