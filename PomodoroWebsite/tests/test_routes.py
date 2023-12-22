import unittest
from flask_testing import TestCase
from app.models import db
from app.app import create_app

class RoutesTestCase(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Pomodoro App!', response.data.decode())

    # Additional tests for other routes...

if __name__ == '__main__':
    unittest.main()
