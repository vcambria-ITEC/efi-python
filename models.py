from app import db

from flask_login import UserMixin

from datetime import datetime
import pytz

arg_timezone = pytz.timezone('America/Argentina/Buenos_Aires')

def get_arg_datetime():
    return datetime.now(arg_timezone)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True) 

    def __str__(self):
        return self.username
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=get_arg_datetime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    author = db.relationship('User', backref='posts', lazy=True)

    comments = db.relationship('Comment', backref='posts', lazy=True)

    def __str__(self):
        return f"{self.title} {self.content} {self.date}"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)


