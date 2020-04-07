from load_palletes_from_lospec import load_palettes
from posts import load_posts

from flask import make_response, jsonify, render_template

from app import app, get_db_session, login_manager
from app.models import Post, User
from app.forms import RegisterForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    session = get_db_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    posts = get_db_session().query(Post).all()
    return render_template('all_posts.html', title='Главная', posts=posts)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Главная', form=form)


@app.route('/registration')
def registration():
    form = RegisterForm()
    return render_template('registration.html', title='Главная', form=form)


if __name__ == '__main__':
    app.run()
