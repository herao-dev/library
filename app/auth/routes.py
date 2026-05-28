from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_current_user, jwt_required
from app.auth import auth_bp
from app.models.user import User
from app.extensions import db


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "请提供登录信息"}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"success": False, "message": "用户名或密码错误"}), 401

    if not user.is_active:
        return jsonify({"success": False, "message": "该账号已被禁用，请联系管理员"}), 403

    additional_claims = {"role": user.role}
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )

    return jsonify({
        "success": True,
        "message": "登录成功",
        "data": {
            "access_token": access_token,
            "user": user.to_dict()
        }
    })


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "请提供注册信息"}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not username or not email or not password:
        return jsonify({"success": False, "message": "请填写所有必填字段"}), 400

    if len(username) < 2 or len(username) > 64:
        return jsonify({"success": False, "message": "用户名长度应为2-64个字符"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "message": "密码长度不能少于6位"}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "两次密码输入不一致"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "该用户名已被注册"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "该邮箱已被注册"}), 400

    user = User(username=username, email=email, role='user')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "注册成功，请登录"
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "message": "用户不存在"}), 404
    return jsonify({
        "success": True,
        "data": user.to_dict()
    })
