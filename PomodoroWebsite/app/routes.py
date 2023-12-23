from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
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

@routes.route('/index')
def index():
    settings_applied = session.get('settings_applied', False)
    return render_template('index.html', settings_applied=settings_applied)


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
        session['userid'] = user.userid
        session['settings_applied'] = False
        return redirect(url_for('routes.index'))
    else:
        flash("Invalid username or password")
        return redirect(url_for('routes.login'))
    
@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

    
@routes.route('/start_pomodoro', methods=['POST'])
def start_pomodoro():
    # Check if user is logged in
    if 'userid' not in session:
        flash("Please log in to continue.")
        return redirect(url_for('routes.login'))

    userid = session['userid']
    work_interval = request.form.get('workInterval')
    short_break_interval = request.form.get('shortBreakInterval')
    long_break_interval = request.form.get('longBreakInterval')

    settings = PomodoroSettings.query.filter_by(UserID=userid).first()
    if settings:
        settings.WorkInterval = work_interval
        settings.ShortBreakInterval = short_break_interval
        settings.LongBreakInterval = long_break_interval
    else:
        new_settings = PomodoroSettings(
            UserID=userid,
            WorkInterval=work_interval,
            ShortBreakInterval=short_break_interval,
            LongBreakInterval=long_break_interval
        )
        db.session.add(new_settings)

    try:
        db.session.commit()
        flash('Pomodoro settings updated successfully.')
        session['settings_applied'] = True

    except Exception as e:
        db.session.rollback()
        flash('Failed to update settings: ' + str(e))

    return redirect(url_for('routes.index'))



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
    
@routes.route('/get_user_logs/<username>', methods=['GET'])
def get_user_logs(username):
    query = """
    SELECT u.username, pl.LogID, pl.Note
    FROM users u
    JOIN PomodoroLogs pl ON u.userid = pl.UserID
    WHERE u.username = :username
    """
    
    result = db.session.execute(query, {"username": username})
    
    logs = result.fetchall()
    
    if logs:
        logs_list = [{"username": log.username, "LogID": log.LogID, "Note": log.Note} for log in logs]
        return jsonify(logs_list)
    else:
        return jsonify({"message": "No logs found for the user"}), 404

