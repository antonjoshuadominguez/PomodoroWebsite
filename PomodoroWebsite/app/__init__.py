from flask import Flask
from .models import db
from .routes import routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
    db.init_app(app)
    
    app.register_blueprint(routes)

    return app
