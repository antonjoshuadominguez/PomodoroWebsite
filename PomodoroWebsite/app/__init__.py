from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

    app.register_blueprint(routes)

    return app
