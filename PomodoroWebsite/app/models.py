from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()

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

class UserSettingsView(Base):
    __tablename__ = 'UserSettingsView'
    username = db.Column(db.Text, primary_key=True)
    WorkInterval = db.Column(db.Integer)
    ShortBreakInterval = db.Column(db.Integer)
    LongBreakInterval = db.Column(db.Integer)

class ProcedureView(Base):
    __tablename__ = 'ProcedureView'
    username = db.Column(db.Text, primary_key=True)
    TotalSessions = db.Column(db.Integer)
    AverageWorkInterval = db.Column(db.Integer)