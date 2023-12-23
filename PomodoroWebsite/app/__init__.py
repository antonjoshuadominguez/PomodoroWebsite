from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from .models import db
from .routes import routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'maytapasar'

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

        # Drop the view if it exists and then create it
        drop_view_sql = text("DROP VIEW IF EXISTS UserSettingsView")
        create_view_sql = text("""
            CREATE VIEW UserSettingsView AS
            SELECT
                u.username AS username,
                ps.WorkInterval AS WorkInterval,
                ps.ShortBreakInterval AS ShortBreakInterval,
                ps.LongBreakInterval AS LongBreakInterval
            FROM
                users u
            JOIN
                PomodoroSettings ps ON u.userid = ps.UserID
        """)

        with db.engine.connect() as conn:
            conn.execute(drop_view_sql)
            conn.execute(create_view_sql)

    app.register_blueprint(routes)

    return app
