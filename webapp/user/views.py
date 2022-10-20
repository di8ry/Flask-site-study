from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, current_user
from webapp.user.forms import LoginForm, RegForm
from webapp.user.models import User
from webapp.db import db

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Авторизация'
    form = LoginForm()
    global backref
    backref = request.referrer
    print(backref)
    return render_template(
        'login.html',
        title=title,
        form=form
    )


@blueprint.route('/process_login', methods=['POST'])
def process_login():
    form = LoginForm()
    user = User.query.filter(User.username == form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('Welcome back')
        global backref
        return redirect(backref)
    flash('Wrong username or password')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('See you next time')
    return redirect(url_for('news.index'))


@blueprint.route('/reg')
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    form = RegForm()
    return render_template(
        'reg.html',
        title=title,
        form=form
    )


@blueprint.route('/process_reg', methods=['POST'])
def process_reg():
    form = RegForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            status='user'
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Успешно зарегистрированы')
        return redirect(url_for('user.login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Ошибка в поле {field}: {error}')
    return redirect(url_for('user.reg'))

