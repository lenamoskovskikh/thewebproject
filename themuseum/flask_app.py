import datetime
import json
import random
from flask import Flask, render_template, redirect, request
from extra_files.finder import get_png
from data import db_session
from data.users import User
from data.forms import RegisterForm, LoginForm, RecoveryForm, FinalRecoveryForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
msg = MIMEMultipart()


def get_image():
    if current_user.is_authenticated and os.path.exists(f'static/img/photo_profile/{current_user.id}.png'):
        return f'img/photo_profile/{current_user.id}.png'
    else:
        return f'img/photo_profile/00.png'


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    return render_template("main.html", title='Главная', photo=get_image())


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template('profile.html', title='Профиль пользователя', photo=get_image())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form, photo=get_image())
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают", photo=get_image())
        pswd = form.password.data
        if len(pswd) > 20 or len(pswd) < 8 or pswd.isdigit() or pswd.islower():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Пароль не надёжный", photo=get_image())
        pswd = None
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="такой пользователь существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/places')
def show_places():
    coords = [["151.215484%2C-33.857376", '18', 'opera.jpg', 'Здание оперы в Сиднее'],
              ["-74.011603%2C40.711530", '18', 'oculus.jpg', 'Транспортный узел Oculus в Нью-Йорке'],
              ["103.866095%2C1.281537", '18', 'garden.jpg', '"Gardens by the Bay" парк деревьев в Сингапуре'],
              ["55.274247%2C25.197180", '18', 'halifa.jpg', 'Бурдж-Халифа'],
              ["37.618879%2C55.751426", '18', 'msc.jpg', 'Московский Кремль'],
              ["139.811626%2C35.709850", '18', 'tokyo.jpg', 'Токио Скай-три']]
    images = []
    for el in coords:
        img = get_png(*el[:-1])
        images.append([img, el[-1]])
    return render_template("places.html", title='красивые места', images=images, photo=get_image())


@app.route('/cities')
def cities():
    return render_template("cities.html", title="удивительные города")


@app.route('/cities/peking')
def peking():
    return render_template("peking.html", title="ПЕКИН")


@app.route('/cities/tokyo')
def tokyo():
    return render_template("tokyo.html", title="ТОКИО")


@app.route('/cities/hongkong')
def hongkong():
    return render_template("hongkong.html", title="ГОНКОНГ")


@app.route('/cities/paris')
def paris():
    return render_template("paris.html", title="ПАРИЖ")


@app.route('/cities/newyork')
def new_york():
    return render_template("new_york.html", title="НЬЮ-ЙОРК")


@app.route('/cities/singapore')
def singapore():
    return render_template("singapore.html", title="СИНГАПУР")


@app.route('/cities/oslo')
def oslo():
    return render_template("oslo.html", title="ОСЛО")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html", title='Ошибка 404')


@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", title='Ошибка 500')


def main():
    name_db = 'webproject.db'
    db_session.global_init(f"db/{name_db}")
    app.run()


if __name__ == '__main__':
    main()
