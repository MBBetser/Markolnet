from flask import Blueprint, request, jsonify
from ..db import *
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user

user_routes = Blueprint('user_routes', __name__, url_prefix='/users')
@user_routes.route('/')
def test():
    return 'Hey from users route!'

@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 409
    else:
        user = User(username=username, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201


@user_routes.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return "Login route works with GET"

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    
    
@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200

@user_routes.route('/protected')
@login_required
def protected():
    return f'Hello, {current_user.username}!'
