from flask import Blueprint, request, jsonify, session
from ..db import *
from ..models import *

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
    
    if get_user_by_username(username):
        return jsonify({"message": "User already exists"}), 409
    else:
        add_user(username, password, user_type)
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
    
    user = get_user_by_username(username)
    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    
@user_routes.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@user_routes.route('/profile')
def profile():
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        return jsonify(user), 200
    else:
        return jsonify({"message": "Not logged in"}), 401