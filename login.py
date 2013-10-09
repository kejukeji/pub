# coding: utf-8

from flask import redirect
from flask.ext.login import LoginManager, login_required, login_user, logout_user

from models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


def login():
    user = User.query.filter(User.id == 1).first()
    login_user(user)
    return redirect('/admin')  # todo-lyw change later


@login_required
def setting():
    pass


@login_required
def logout():
    logout_user()
    return redirect('/admin')  # todo-lyw 需要更好的地方