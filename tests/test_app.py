import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from util.db import db
from config import Config

class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WEATHER_API_KEY = "test_key"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize the database."""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pardeep', response.data) # Check for some content

if __name__ == '__main__':
    unittest.main()
