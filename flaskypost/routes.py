from flask import render_template, url_for, flash
from flaskypost import app
from flaskypost.forms import RegistrationForm, LoginForm
from flaskypost.models import User, Post

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
    }
]


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
