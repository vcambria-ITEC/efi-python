from repositories.user_repository import get_by_id

def get_user_role(self, user_id):
    user = get_by_id(user_id)
    return user.credential.role