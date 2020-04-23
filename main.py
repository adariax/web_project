from flask import render_template, redirect, request
from flask_login import login_required, logout_user, login_user

from app import app, get_db_session, login_manager
from app.models import User
from app.forms import RegisterForm, PostForm

import logging

from loading_posts import load_posts

# loading all posts from the group wall
load_posts(app.config['ACCESS_TOKEN'], app.config['VK_GROUP_ID'], get_db_session())

logging.getLogger('serializer').setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)

# static params for pages templates
VK_PARAMS = {
    'group_id': app.config['VK_GROUP_ID'],
    'client_id': app.config['CLIENT_ID'],
    'screen_name': app.config['VK_SCREEN_NAME'],
    'group_name': app.config['VK_GROUP_NAME']
}


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error, **VK_PARAMS), 404


@app.errorhandler(401)
def login_error(error):
    return render_template('error.html', error=error, **VK_PARAMS), 401


@login_manager.user_loader
def load_user(user_id):
    db_session = get_db_session()
    return db_session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('all_posts.html', title='Главная', **VK_PARAMS)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    args = request.args
    if args:
        db_session = get_db_session()
        user = db_session.query(User).filter(User.vk_domain == args.get('uid')).first()
        if not user:
            return render_template('login.html', title='Вход',
                                   message="Такой пользователь не зарегистрирован",
                                   **VK_PARAMS)
        login_user(user)
        return redirect("/")
    return render_template('login.html', title='Вход', **VK_PARAMS)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    return render_template('registration.html', title='Регистрация', form=form, **VK_PARAMS)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    return render_template('post.html', title='Новая запись', form=form, **VK_PARAMS)


@app.route('/fav_posts', methods=['GET', 'POST'])
@login_required
def fav_posts():
    form = PostForm()
    return render_template('fav_posts.html', title='Избранное', form=form, **VK_PARAMS)


@app.route('/sug_posts', methods=['GET', 'POST'])
@login_required
def sug_posts():
    return render_template('sug_posts.html', title='Предложенные записи', **VK_PARAMS)


if __name__ == '__main__':
    app.run()
