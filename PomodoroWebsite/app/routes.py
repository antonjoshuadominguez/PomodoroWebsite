from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from .models import db, User, PomodoroSettings, UserSettingsView, PomodoroLogs
from sqlalchemy import text

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    settings_applied = session.get('settings_applied', False)
    saved_note = ''
    user_notes = []

    if 'userid' in session:
        userid = session['userid']
        # Fetch the most recent note of the logged-in user
        user_notes = PomodoroLogs.query.filter_by(UserID=userid).order_by(PomodoroLogs.LogID.desc()).all()

    return render_template('index.html', settings_applied=settings_applied, user_notes=user_notes)



@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/register')
def register():
    return render_template('register.html')

@routes.route('/create_user', methods=['POST'])
def create_user():
    username = request.form['username']
    password = request.form['password']
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

@routes.route('/add_note', methods=['POST'])
def add_note():
    if 'userid' not in session:
        flash("Please log in to add notes.")
        return redirect(url_for('routes.login'))

    note = request.form.get('note')
    userid = session['userid']

    new_note = PomodoroLogs(UserID=userid, Note=note)
    db.session.add(new_note)

    try:
        db.session.commit()
        flash('Note added successfully.')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add note: ' + str(e))

    return redirect(url_for('routes.index'))

@routes.route('/delete_note/<int:LogID>')
def delete_note(LogID):
    if 'userid' not in session:
        flash("Please log in to delete notes.")
        return redirect(url_for('routes.login'))

    note_to_delete = PomodoroLogs.query.get(LogID)
    if note_to_delete and note_to_delete.UserID == session['userid']:
        db.session.delete(note_to_delete)
        try:
            db.session.commit()
            flash('Note deleted successfully.')
        except Exception as e:
            db.session.rollback()
            flash('Failed to delete note: ' + str(e))
    else:
        flash('Note not found or access denied.')

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
    
@routes.route('/user_settings')
def user_settings():
    if 'userid' not in session:
        flash("Please log in to view user settings.")
        return redirect(url_for('routes.login'))

    userid = session['userid']
    settings = UserSettingsView.query.filter_by(userid=userid).all()
    return render_template('user_settings.html', user_settings=settings)

    
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
    
@routes.route('/display_user_settings')
def display_user_settings():
    user_settings = []

    view_data = db.session.execute(text("SELECT username, WorkInterval, ShortBreakInterval, LongBreakInterval FROM UserSettingsView;"))
    
    for row in view_data.fetchall():
        user_settings.append({
            'username': row[0],
            'WorkInterval': row[1],
            'ShortBreakInterval': row[2],
            'LongBreakInterval': row[3]
        })

    return render_template('user_settings.html', user_settings=user_settings)


