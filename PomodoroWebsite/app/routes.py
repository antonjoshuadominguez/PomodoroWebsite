from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from .models import db, User, PomodoroSettings, UserSettingsView

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
    username = request.form['username']
    password = request.form['password']  # Directly using the password without hashing
    email = request.form['email']

    new_user = User(username=username, password=password, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully.')
        return redirect(url_for('routes.login'))
    except Exception as e:
        db.session.rollback()
        flash('Registration failed: ' + str(e))
        return redirect(url_for('routes.register'))


@routes.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@routes.route('/get_user_settings/<username>', methods=['GET'])
def get_user_settings(username):
    user_settings = UserSettingsView.query.filter_by(username=username).first()
    if user_settings:
        return jsonify({
            "username": username,
            "WorkInterval": user_settings.WorkInterval,
            "ShortBreakInterval": user_settings.ShortBreakInterval,
            "LongBreakInterval": user_settings.LongBreakInterval
        })
    else:
        return jsonify({"message": "User settings not found"}), 404

