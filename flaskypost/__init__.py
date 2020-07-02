from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskypost.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
mail = Mail(app)


from flaskypost.users.routes import users
from flaskypost.posts.routes import posts
from flaskypost.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)