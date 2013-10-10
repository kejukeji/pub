# coding: utf-8

from flask.ext import restful
from flask.ext.restful import reqparse

from models import db, User
from models import UserInfo as UserInfoDb  # 避免和下面的类冲突
from utils import pickler


class UserRegister(restful.Resource):
    """用户注册的接口"""

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('login_type', type=int, required=True, help=u'缺少参数 login_type必须为 0（注册用户），1（微博用户），2（QQ用户）')
        parser.add_argument('nick_name', type=str, required=True, help=u'缺少参数 nick_name必须唯一')
        parser.add_argument('password', type=str, required=False)
        parser.add_argument('login_name', type=str, required=False)
        parser.add_argument('open_id', type=str, required=False)
        args = parser.parse_args()

        login_type = args.get('login_type')
        nick_name = args.get('nick_name')
        password = args.get('password', None)
        login_name = args.get('login_name', None)
        open_id = args.get('open_id', None)

        err = {}

        if login_type == 0:  # 注意纯数字的昵称和手机号的冲突，以后不同用户的昵称和不能用户登录名不能相同，同一个用户可以
            if not password:
                err['message'] = '注册用户必须要有密码'
                return err
            if not login_name:
                err['message'] = '注册用户必须有登陆名'
                return err
            if nick_name.count('@'):
                err['message'] = 'nick_name不能包含@符号'
                return err

            if User.query.filter(User.login_name == login_name).count():
                err['message'] = 'login_name已重复'
                return err
            if User.query.filter(User.nick_name == login_name).count():
                err['message'] = 'login_name已重复'
                return err
            if User.query.filter(User.nick_name == nick_name).count():
                err['message'] = 'nick_name已重复'
                return err
            if User.query.filter(User.login_name == nick_name).count():
                err['message'] = 'nick_name已重复'
                return err

            user = User(login_type=login_type, nick_name=nick_name, password=password, login_name=login_name)
            db.add(user)
            db.commit()
            user = User.query.filter(User.login_name == login_name).first()
            user_info = UserInfoDb(user_id=user.id)
            if login_name.count('@'):
                user_info.email = login_name
            db.add(user_info)
            db.commit()

        if login_type == 1 or login_type == 2:
            if not open_id:
                err['message'] = '第三方登陆用户必须有open_id'
                return err
            if nick_name.count('@'):
                err['message'] = 'nick_name不能包含@符号'
                return err

            if User.query.filter(User.open_id == open_id).count():
                err['message'] = 'open_id已重复'
                return err
            if User.query.filter(User.nick_name == nick_name).count():
                err['message'] = 'nick_name已重复'
                return err

            user = User(login_type=login_type, nick_name=nick_name, open_id=open_id)
            db.add(user)
            db.commit()
            user = User.query.filter(User.login_name == login_name).first()
            user_info = UserInfoDb(user_id=user.id)
            db.add(user_info)
            db.commit()

        return pickler.flatten(User.query.filter(User.nick_name == nick_name).first())


class UserLogin(restful.Resource):
    """用户登陆"""

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('login_type', type=int, required=True, help=u'登陆必须需要login_type')
        parser.add_argument('user_name', type=str, required=False)
        parser.add_argument('password', type=str, required=False)
        parser.add_argument('open_id', type=str, required=False)
        args = parser.parse_args()

        login_type = args.get('login_type')
        user_name = args.get('user_name', None)
        password = args.get('password', None)
        open_id = args.get('open_id', None)

        err = {}

        if login_type == 0:
            if not password:
                err['message'] = '登陆用户必须有密码'
                return err
            if not user_name:
                err['message'] = '登陆用户必须有账号名user_name，可以是登录名，可以是昵称'
                return err
            if User.query.filter(User.nick_name == user_name).count():
                user = User.query.filter(User.nick_name == user_name).first()
            elif User.query.filter(User.login_name == user_name).count():
                user = User.query.filter(User.login_name == user_name).first()
            else:
                err['message'] = '用户不存在'
                return err

            if user.check_password(password):
                return pickler.flatten(user)
            else:
                err['message'] = '密码错误'
                return err

        if login_type == 1:
            if not open_id:
                err['message'] = '微博第三方登陆必须需要open_id'
                return err
            if User.query.filter(User.login_type == 1, User.open_id == open_id).count():
                user = User.query.filter(User.login_type == 1, User.open_id == open_id)
            else:
                err['message'] = '不存在这个open_id'
                return err

            return pickler.flatten(user)

        if login_type == 2:
            if not open_id:
                err['message'] = '微博第三方登陆必须需要open_id'
                return err
            if User.query.filter(User.login_type == 2, User.open_id == open_id).count():
                user = User.query.filter(User.login_type == 2, User.open_id == open_id)
            else:
                err['message'] = '不存在这个open_id'
                return err

            return pickler.flatten(user)


class UserInfo(restful.Resource):
    """获取和设置用户消息"""

    def post(self, user_id):
        pass