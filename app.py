import requests

from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Imports para el sistema de login
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
    )



app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:@localhost/db_miniblog"
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

from models import User, Post, Comment

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/register')
def register():
    return render_template(
        'auth/register.html'
    )

@app.route('/login')
def login():
    return render_template(
        'auth/login.html'
    )

@app.route('/create_post')
def posts():
    return render_template(
        'create_post.html'
    )

if __name__ == '__main__':
    app.run(debug=True)