import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, request, redirect
from flaskypost import app, db, bcrypt
from flaskypost.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Wrong email or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_image_for_user(_image):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(_image.filename)
    img_fn = rand_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/profile_images', img_fn)

    output_size = (125, 125)
    i = Image.open(_image)
    i.thumbnail(output_size)
    i.save(img_path)

    return img_fn


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            _img = save_image_for_user(form.image.data)
            current_user.image = _img
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Successfully!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_images/' + current_user.image)
    return render_template('profile.html', image_file=image_file, form=form)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    return render_template('newPost.html')
