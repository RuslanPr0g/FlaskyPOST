from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '25613c65532b1973abc984a0faa7aecf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flpst.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskypost import routes
