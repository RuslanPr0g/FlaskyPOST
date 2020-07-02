from flask import render_template, request, Blueprint
from flaskypost.models import Post

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('index.html', posts=posts)
