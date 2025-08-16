import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    CLIENT_ID = os.environ.get('CLIENT_ID') or 'default-client-id'
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or 'default-client-secret'
    ACCESS_TOKEN_URL = os.environ.get('ACCESS_TOKEN_URL') or "https://oauth2.googleapis.com/token"

config = Config()
