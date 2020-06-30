from flask import render_template, url_for, flash, redirect
from flaskypost import app, db, bcrypt
from flaskypost.forms import RegistrationForm, LoginForm
from flaskypost.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Ruslan',
        'title': 'Welcome',
        'content': 'This is the first post.',
        'date_posted': 'June 29, 2020'
    },
    {
        'author': 'Vlad',
        'title': 'Join',
        'content': 'WOw, I have joined here!',
        'date_posted': 'June 30, 2020'
    },
    {
        'author': 'Vlad',
        'title': 'Join',
        'content': 'WOw, I have joined here!',
        'date_posted': 'June 30, 2020'
    },
    {
        'author': 'Vlad',
        'title': 'Join',
        'content': 'WOw, I have joined here!',
        'date_posted': 'June 30, 2020'
    },
    {
        'author': 'Vlad',
        'title': 'Join',
        'content': 'WOw, I have joined here!',
        'date_posted': 'June 30, 2020'
    },
    {
        'author': 'Vlad',
        'title': 'Join',
        'content': 'WOw, I have joined here!',
        'date_posted': 'June 30, 2020'
    }
]


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Wrong email or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
