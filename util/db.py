from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Todo(db.Model,UserMixin):
    __tablename__ = 'todo'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE') ,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date =  db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='todo', lazy=True)

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='user')

class Webpage(db.Model):
    __tablename__ = 'webpage'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date =  db.Column(db.DateTime, default=datetime.utcnow)
 
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), nullable=False)
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ActivityLog {self.user_email} - {self.action}>'