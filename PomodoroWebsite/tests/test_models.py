import unittest
from app.models import db, User, PomodoroSettings, PomodoroLogs, UserSettingsView
from app.app import create_app

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser', password='testpass', email='test@test.com')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, 'testuser')

    # Additional tests for other models...

if __name__ == '__main__':
    unittest.main()
