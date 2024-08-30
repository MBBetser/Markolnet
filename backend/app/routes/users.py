from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..db import *
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user
import requests

user_routes = Blueprint('user_routes', __name__, url_prefix='/users')


@user_routes.route('/') 
def users():
    return render_template('users.html')

@user_routes.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phone_number')
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    user_type = 'customer'


    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    else:
        user = User(username=username,
                    password=password,
                    phone_number=phone_number,
                    email=email,
                    longitude=longitude,
                    latitude=latitude,
                    user_type=user_type)
        
        db.session.add(user)
        db.session.commit()
        store_data = {
            'owner_id': user.id,
            'name': f"{username}'s Store"
        }
        store_creation_response = requests.post(url_for('stores_route.create_store', _external=True), json=store_data)

        if store_creation_response.status_code != 200:
            return jsonify({"message": "User created, but failed to create store"}), 500

        return jsonify({"redirect_url":url_for('user_routes.login')})


@user_routes.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('users.html')

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return jsonify({"redirect_url":url_for('index')})
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')

@user_routes.route('/protected')
@login_required
def protected():
    return f'Hello, {current_user.username}!'

@user_routes.route('/remove-<int:user_id>')
def remove_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200