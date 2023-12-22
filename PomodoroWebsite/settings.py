from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy with a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database models based on the provided schema
class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)

class PomodoroSettings(db.Model):
    __tablename__ = 'PomodoroSettings'
    SettingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.userid'))
    WorkInterval = db.Column(db.Integer, default=25)
    ShortBreakInterval = db.Column(db.Integer, default=5)
    LongBreakInterval = db.Column(db.Integer, default=15)

class PomodoroLogs(db.Model):
    __tablename__ = 'PomodoroLogs'
    LogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.userid'))
    Note = db.Column(db.Text)

# Add a route for the root URL
@app.route('/')
def home():
    return 'Welcome to the Pomodoro App!'

# Define a class to represent the UserSettingsView
class UserSettingsView(db.Model):
    __tablename__ = 'UserSettingsView'
    username = db.Column(db.Text, primary_key=True)
    WorkInterval = db.Column(db.Integer)
    ShortBreakInterval = db.Column(db.Integer)
    LongBreakInterval = db.Column(db.Integer)

# Initialize and setup the database
def initialize_database():
    db.create_all()

    with db.engine.connect() as conn:
        # Use SQLAlchemy's text() construct for raw SQL
        conn.execute(text("""
            CREATE VIEW IF NOT EXISTS "UserSettingsView" AS
            SELECT u."username", p."WorkInterval", p."ShortBreakInterval", p."LongBreakInterval"
            FROM "users" u
            JOIN "PomodoroSettings" p ON u."userid" = p."UserID";
        """))

        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS "AfterUserCreation"
            AFTER INSERT ON "users"
            BEGIN
                INSERT INTO "PomodoroSettings" ("UserID") VALUES (NEW."userid");
            END;
        """))

# Define example routes
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/get_user_settings/<username>', methods=['GET'])
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

# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        initialize_database()  # Initialize the database within the application context
    app.run(debug=True)