from flask_jwt_extended import get_jwt
from functools import wraps
from utils.exception_utils import ForbiddenError
from utils.message_utils import NOT_PERMISSION_ERROR

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if not role or role not in allowed_roles:
                raise ForbiddenError(NOT_PERMISSION_ERROR)
            return fn(*args, **kwargs)
        return wrapper
    return decorator