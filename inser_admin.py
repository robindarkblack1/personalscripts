import os
from flask import Flask
from util.db import db, User
from config import config

# Initialize Flask app
app = Flask(__name__)

# Set the correct database URI for SQLite in the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app context
db.init_app(app)

def insert_admin():
    """Insert an admin user if not exists"""
    with app.app_context():
        # Ensure database tables exist
        db.create_all()

        # Check if the admin already exists
        existing_admin = User.query.filter_by(email='admin@admin.com').first()
        if existing_admin:
            print("Admin user already exists!")
            return

        # Create a new admin user without hashing the password
        admin = User(
            name='Pardeep',
            email='admin@admin.com',
            password='lol',  # Plain text password (not recommended for production)
            role='admin'
        )

        # Add and commit the admin user
        db.session.add(admin)
        db.session.commit()
        print("Admin user inserted successfully!")

# Run the function
if __name__ == '__main__':
    insert_admin()
