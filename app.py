from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
