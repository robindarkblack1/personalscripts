import unittest
import os
import sys
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from util.db import db, User, File
from config import config

class TestConfig(object):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'
    UPLOAD_FOLDER = 'test_uploads'

class FileFeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create a user
            user = User(name='testuser', email='test@example.com', password='testpassword')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        return self.client.post('/login', data=dict(
            email='test@example.com',
            password='testpassword'
        ), follow_redirects=True)

    def test_files_page(self):
        with self.app.app_context():
            self.login()
            response = self.client.get('/files', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File Sharer', response.data)

if __name__ == '__main__':
    unittest.main()
