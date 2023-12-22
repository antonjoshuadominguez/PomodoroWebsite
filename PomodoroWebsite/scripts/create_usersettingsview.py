from app.models import db

# Define the UserSettingsView model
class UserSettingsView(db.Model):
    __tablename__ = 'UserSettingsView'
    username = db.Column(db.Text, primary_key=True)
    WorkInterval = db.Column(db.Integer)
    ShortBreakInterval = db.Column(db.Integer)
    LongBreakInterval = db.Column(db.Integer)

# Create the table in the database
db.create_all()
