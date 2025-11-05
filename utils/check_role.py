from services.user_service import get_user_by_id

from flask_jwt_extended import get_jwt


def is_owner(current_user_id, resource_owner_id):
    current_user = get_user_by_id(current_user_id)
    resource_owner = get_user_by_id(resource_owner_id)

    if current_user.role == 'admin':
        return True
    return current_user.role == resource_owner.role

def get_role():
    return get_jwt().get('role')