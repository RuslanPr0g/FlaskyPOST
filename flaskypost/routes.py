import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, request, redirect, abort
from flaskypost import app, db, bcrypt, mail
from flaskypost.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskypost.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=6)
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
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('newPost.html', form=form, legend='Create Post')


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Successfully!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newPost.html', form=form, legend='Post Update')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/user/<string:username>')
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('user_page.html', posts=posts, user=user)


def send_token_by_email(user):
    token = user.get_reset_token()
    message = Message('Reset Password Request.',
                      sender='theruslanrudenko1992@gmail.com', recipients=[user.email])
    message.body = f''' 
Reset Password Link: {url_for('password_reset', token=token, _external=True)}
If you haven't made this request, just ignore it.
'''
    mail.send(message)


@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_token_by_email(user)
        flash('Please, check your email.', 'success')
        return redirect(url_for('login'))
    return render_template('resetPassword.html', form=form)


@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Time expired or you do not have the access.', 'warning')
        return redirect(url_for('password_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('password_reset_token.html', form=form)
