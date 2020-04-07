from load_palletes_from_lospec import load_palettes
from posts import load_posts

from flask import make_response, jsonify, render_template

from app import app, get_db_session
from app.models import Post


@app.route('/')
@app.route('/index')
def index():
    posts = get_db_session().query(Post).all()
    return render_template('all_posts.html', title='Главная', posts=posts)


if __name__ == '__main__':
    app.run()
