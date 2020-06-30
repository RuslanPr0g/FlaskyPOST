from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '25613c65532b1973abc984a0faa7aecf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flpst.db'
db = SQLAlchemy(app)

from app import routes
