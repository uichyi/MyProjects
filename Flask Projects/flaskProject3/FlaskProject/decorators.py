from functools import wraps
from flask_login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.permission.value < permission:
                return "You do not have permission to access this page."
            return f(*args, **kwargs)
        return decorated_function
    return decorator
