from flask import Flask
from .models import db
from .routes import routes_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
    
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    app.register_blueprint(routes_bp, url_prefix='/')

    return app