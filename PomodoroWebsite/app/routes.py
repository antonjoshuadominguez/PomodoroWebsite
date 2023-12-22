from flask import Blueprint, request, jsonify
from .models import db, User, UserSettingsView

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return 'Welcome to the Pomodoro App!'

@routes.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

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
