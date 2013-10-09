# coding: utf-8

from flask.ext import restful
from flask.ext.restful import reqparse

from models import db, User
from utils import pickler


class UserRegister(restful.Resource):
    """用户注册的接口"""

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('login_type', type=int, required=True, help=u'缺少参数 login_type必须为 0（注册用户），1（微博用户），2（QQ用户）')
        parser.add_argument('nick_name', type=str, required=True, help=u'缺少参数 nick_name必须唯一')
        parser.add_argument('password', type=str, required=False, help=u'如果是注册用户，必须需要密码')
        parser.add_argument('login_name', type=str, required=False, help=u'必须是邮箱或者手机号')
        parser.add_argument('open_id', type=str, required=False)
        args = parser.parse_args()

        login_type = args.get('login_type')
        nick_name = args.get('nick_name')
        password = args.get('password', None)
        login_name = args.get('login_name', None)
        open_id = args.get('open_id', None)

        err = {}

        if login_type == 0:
            if password is None:
                err['password'] = '注册用户必须要有密码'
            if login_name is None:
                err['login_name'] = '注册用户必须有登陆名'
            if nick_name.count('@'):
                err['nick_name'] = 'nick_name不能包含@符号'

            if not err:
                if User.query.filter(User.login_name == login_name).count():
                    err['login_name'] = 'login_name已重复'
                if User.query.filter(User.nick_name == nick_name).count():
                    err['nick_name'] = 'nick_name已重复'

            if not err:
                user = User(login_type=login_type, nick_name=nick_name, password=password, login_name=login_name)
                db.add(user)
                db.commit()

        if login_type == 1 or login_type == 2:
            if open_id is None:
                err['open_id'] = '第三方登陆用户必须有open_id'
            if nick_name.count('@'):
                err['nick_name'] = 'nick_name不能包含@符号'

            if not err:
                if User.query.filter(User.open_id == open_id).count():
                    err['open_id'] = 'open_id已重复'
                if User.query.filter(User.nick_name == nick_name).count():
                    err['nick_name'] = 'nick_name已重复'

            if not err:
                user = User(login_type=login_type, nick_name=nick_name, open_id=open_id)
                db.add(user)
                db.commit()

        if not err:
            return pickler.flatten(User.query.filter(User.nick_name == nick_name).first())
        else:
            return err


class UserLogin(restful.Resource):
    """用户登陆"""

    def post(self):
        pass


class UserInfo(restful.Resource):
    """获取和设置用户消息"""

    def post(self, user_id):
        pass