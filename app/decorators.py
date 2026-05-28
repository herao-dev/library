from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_current_user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        if not user:
            return jsonify({"success": False, "message": "请先登录"}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        if not user or not user.is_admin:
            return jsonify({"success": False, "message": "权限不足"}), 403
        return f(*args, **kwargs)
    return decorated_function
