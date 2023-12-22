from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, UserSettingsView

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/register')
def register():
    return render_template('register.html')

@routes.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    if 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({"message": "Missing data fields"}), 400

    try:
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password=hashed_password, email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username or email already exists"}), 409

@routes.route('/login_user', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@routes.route('/get_user_settings/<username>', methods=['GET'])
def get_user_settings(username):
    settings = db.session.query(UserSettingsView).filter_by(username=username).first()
    if settings:
        return jsonify({
            "username": settings.username,
            "WorkInterval": settings.WorkInterval,
            "ShortBreakInterval": settings.ShortBreakInterval,
            "LongBreakInterval": settings.LongBreakInterval
        })
    else:
        return jsonify({"message": "User not found"}), 404
