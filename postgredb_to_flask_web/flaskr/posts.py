from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

posts = Blueprint('posts', __name__)

@posts.route('/posts')
def get_popular_posts():
    return 'Posts Page!'
