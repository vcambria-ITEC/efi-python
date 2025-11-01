from services.user_service import get_user_by_id

def get_user_role(self, user_id):
    user = get_user_by_id(user_id)
    return user.credential.role