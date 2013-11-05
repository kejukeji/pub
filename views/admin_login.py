# coding: utf-8

"""用户登陆相关"""

from flask import redirect, render_template, request
from wtforms import form, fields, validators
from flask.ext import login
from flask.ext.admin import helpers

from ..models import User, db
from pub_app import app


class LoginForm(form.Form):
    """定义用户登陆的Form"""

    user_name = fields.TextField(u'昵称或邮箱', validators=[validators.required()])
    password = fields.PasswordField(u'密码', validators=[validators.required()])

    def validate_user_name(self, field):
        user = self.get_user()
        if not user:
            raise validators.ValidationError('用户名不存在')

        if not user.check_password(self.password.data):
            raise validators.ValidationError('密码错误')

    def get_user(self):
        user = User.query.filter(User.nick_name == self.user_name.data).first()
        if not user:
            user = User.query.filter(User.login_name == self.user_name.data).first()
        return user


class RegisterForm(form.Form):
    """定义用户注册的form"""

    login = fields.TextField(u'昵称', validators=[validators.required()])  # nick_name
    email = fields.TextField(u'邮箱')  # login_name
    password = fields.PasswordField(u'密码', validators=[validators.required()])  # password

    def validate_login(self, field):
        if User.query.filter(User.nick_name == field.data).count() > 0:
            raise validators.ValidationError(u'昵称重复')
        if User.query.filter(User.login_name == field.data).count() > 0:
            raise validators.ValidationError(u'昵称重复')

    def validate_email(self, field):
        if User.query.filter(User.login_name == field.data).count() > 0:
            raise validators.ValidationError(u'邮箱重复')
        if User.query.filter(User.nick_name == field.data).count() > 0:
            raise validators.ValidationError(u'邮箱重复')


class MyAnonymousUser(object):
    """This is the default object for representing an anonymous user."""

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return True

    def get_id(self):
        return

    def is_admin(self):
        return False

login_manager = login.LoginManager()
login_manager.setup_app(app)

login_manager.anonymous_user = MyAnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


def login_view():
    login_form = LoginForm(request.form)
    if helpers.validate_form_on_submit(login_form):
        user = login_form.get_user()
        login_user_with_remember(user)
        if user.admin:
            return redirect('/admin')  # todo-lyw 这里不该使用绝对编码

        return redirect('/admin')

    return render_template('admin_pub/auth.html', form=login_form)


def register_view():
    register_form = RegisterForm(request.form)
    if helpers.validate_form_on_submit(register_form):
        user = User(login_name=register_form.email.data, password=register_form.password.data,
                    login_type=0, nick_name=register_form.login.data)
        db.add(user)
        db.commit()

        login_user_with_remember(user)
        if user.admin:
            return redirect('/admin')

        return redirect('/admin')

    return render_template('admin_pub/auth.html', form=register_form)


@login.login_required
def logout_view():
    login.logout_user()
    return redirect('/admin')


def login_user_with_remember(user):
    """检查form字段的内容是否记录用户自动登陆"""

    if request.form.get('remember', None):
        login.login_user(user, remember=True)

    login.login_user(user, remember=False)