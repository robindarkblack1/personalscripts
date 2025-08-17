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

    def test_file_upload_download_delete(self):
        with self.app.app_context():
            self.login()
            # Test file upload
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(b'test data')
                temp_file_path = temp_file.name

            with open(temp_file_path, 'rb') as f:
                response = self.client.post('/upload', data=dict(
                    file=(f, 'test.txt')
                ), follow_redirects=True, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File successfully uploaded', response.data)

            # Verify file in database
            uploaded_file = File.query.first()
            self.assertIsNotNone(uploaded_file)
            self.assertEqual(uploaded_file.filename, 'test.txt')

            # Test file download
            response = self.client.get(f'/download/{uploaded_file.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'test data')

            # Test file deletion
            response = self.client.post(f'/delete_file/{uploaded_file.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File successfully deleted', response.data)

            # Verify file is deleted from database
            deleted_file = File.query.first()
            self.assertIsNone(deleted_file)

            # Clean up the temporary file
            os.remove(temp_file_path)

if __name__ == '__main__':
    unittest.main()
