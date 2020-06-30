from models import User, Post
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = '25613c65532b1973abc984a0faa7aecf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flpst.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(
            f'Successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'theruslan.prog@gmail.com' and form.password.data == '12345':
            flash('Successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Wrong email or password.', 'danger')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
