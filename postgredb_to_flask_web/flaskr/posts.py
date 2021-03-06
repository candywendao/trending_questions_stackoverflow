from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.db import Post
from sqlalchemy import and_, or_

bp = Blueprint('posts', __name__)

metric_to_column = {
    "total_votes": Post.total_votes,
    "total_comments": Post.total_comments,
    "7d_favorites": Post.num_favorites_7d,
    "14d_favorites": Post.num_favorites_14d,
    "28d_favorites": Post.num_favorites_28d,
    "7d_comments": Post.num_comments_7d,
    "14d_comments": Post.num_comments_14d,
    "28d_comments": Post.num_comments_28d
}

@bp.route('/posts', methods=("GET", "POST"))
def get_popular_posts():
    if request.method == "GET":
        return render_template('posts.html', posts=[])


    tags = request.form["tags"]
    if tags is not None:
        tags = tags.lower().split()
    else:
        tags = []

    metrics = request.form["metrics"]
    post_column = metric_to_column[metrics]

    posts = Post.query.filter(and_(*[Post.tags.contains(\
        "{" + "{0}".format(tag) + "}", autoescape=True) for tag in tags
    ])).filter(\
        post_column != None\
    ).order_by(post_column.desc()\
    ).limit(10)
    return render_template('posts.html', posts=posts)

@bp.route('/')
def index():
    return "Welcome To Stack Overflow Popular Posts"
