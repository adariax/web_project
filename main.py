from load_palletes_from_lospec import load_palettes
from posts import load_posts

from flask import render_template, redirect
from flask_login import login_required, logout_user, login_user

from app import app, get_db_session, login_manager
from app.models import User
from app.forms import RegisterForm, LoginForm, PostForm


@login_manager.user_loader
def load_user(user_id):
    db_session = get_db_session()
    return db_session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('all_posts.html', title='Главная')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session = get_db_session()
        user = db_session.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Вход',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    return render_template('new_post.html', title='Новая запись', form=form)


if __name__ == '__main__':
    app.run()
