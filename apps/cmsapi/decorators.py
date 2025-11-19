from functools import wraps
from flask import g
from utils import restful

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(g, "user")
            if not user:
                return restful.unlogin_error()
            if user.has_permission(permission):
                return f(*args, **kwargs)
            else:
                return restful.permission_error(message="无权限访问！")
        return decorated_function
    return decorator