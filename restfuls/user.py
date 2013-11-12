# coding: utf-8

import os

from flask.ext import restful
from flask.ext.restful import reqparse
import werkzeug
from werkzeug import secure_filename

from models import db, User
from models import UserInfo as UserInfoDb  # 避免和下面的类冲突
from utils import pickler, todayfstr, allowed_file_extension, time_file_name
from ex_var import HEAD_PICTURE_ALLOWED_EXTENSION, HEAD_PICTURE_BASE_PATH, HEAD_PICTURE_UPLOAD_FOLDER
from utils.others import get_address, flatten


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

        err = {'status': 1}

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

        return_user = User.query.filter(User.nick_name == nick_name).first()
        return wrap_user_json(return_user)


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

        err = {'status': 1}

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
                return {'user': flatten(user), 'status': 0}
            else:
                err['message'] = '密码错误'
                return err

        if login_type == 1:
            if not open_id:
                err['message'] = '微博第三方登陆必须需要open_id'
                return err
            if User.query.filter(User.login_type == 1, User.open_id == open_id).count():
                user = User.query.filter(User.login_type == 1, User.open_id == open_id).first()
            else:
                err['message'] = '不存在这个open_id'
                return err

            return wrap_user_json(user)

        if login_type == 2:
            if not open_id:
                err['message'] = '微博第三方登陆必须需要open_id'
                return err
            if User.query.filter(User.login_type == 2, User.open_id == open_id).count():
                user = User.query.filter(User.login_type == 2, User.open_id == open_id).first()
            else:
                err['message'] = '不存在这个open_id'
                return err

            return wrap_user_json(user)


class UserInfo(restful.Resource):  # todo-lwy 获取消息，二值性使用True和false，设置消息使用1和0
    """获取和设置用户消息"""

    @staticmethod
    def post(user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('login_type', type=int, required=False)
        parser.add_argument('password', type=str, required=False)
        parser.add_argument('open_id', type=str, required=False)
        parser.add_argument('new_password', type=str, required=False)
        parser.add_argument('login_name', type=str, required=False)
        parser.add_argument('nick_name', type=str, required=False)
        parser.add_argument('system_message_time', type=int, required=False)
        parser.add_argument('mobile', type=str, required=False)
        parser.add_argument('tel', type=str, required=False)
        parser.add_argument('real_name', type=str, required=False)
        parser.add_argument('sex', type=int, required=False)
        parser.add_argument('birthday_type', type=int, required=False)
        parser.add_argument('birthday', type=str, required=False)
        parser.add_argument('intro', type=str, required=False)
        parser.add_argument('signature', type=str, required=False)
        parser.add_argument('ethnicity_id', type=str, required=False)
        parser.add_argument('company', type=str, required=False)
        parser.add_argument('job', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('province_id', type=str, required=False)
        parser.add_argument('city_id', type=str, required=False)
        parser.add_argument('county_id', type=str, required=False)
        parser.add_argument('street', type=str, required=False)
        parser.add_argument('head_picture', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        login_type = args.get('login_type', None)
        password = args.get('password', None)
        open_id = args.get('open_id', None)
        new_password = args.get('new_password', None)
        login_name = args.get('login_name', None)
        nick_name = args.get('nick_name', None)
        system_message_time = args.get('system_message_time', None)
        mobile = args.get('mobile', None)
        tel = args.get('tel', None)
        real_name = args.get('real_name', None)
        sex = args.get('sex', None)
        birthday_type = args.get('birthday_type', None)
        birthday = args.get('birthday', None)
        intro = args.get('intro', None)
        signature = args.get('signature', None)
        ethnicity_id = args.get('ethnicity_id', None)
        company = args.get('company', None)
        job = args.get('job', None)
        email = args.get('email', None)
        province_id = args.get('province_id', None)
        city_id = args.get('city_id', None)
        county_id = args.get('county_id', None)
        street = args.get('street', None)
        head_picture = args.get('head_picture', None)

        err = {'status': 1}

        if not login_type:
            login_type = get_login_type(user_id)

        if login_type is None:
            err['message'] = '用户不存在'
            return err

        if ((login_type == 0) and (password is None)) or \
                (((login_type == 1) or (login_type == 2)) and (open_id is None)):
            user = User.query.filter(User.id == user_id).first()
            user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()
            if not user:
                err['message'] = '用户不存在'
                return err
            else:
                if not user_info:
                    create_user_info(user.id)
                    user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()
                    user = User.query.filter(User.id == user_id).first()

                return wrap_user_json(user, user_info)

        if login_type == 0:
            if not password:
                err['message'] = '注册用户获取和改变个人资料需要密码'
                return err
            user = User.query.filter(User.id == user_id).first()
            if not user.check_password(password):
                err['message'] = '密码错误'
                return err
            user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()
            if login_name:
                if User.query.filter(User.login_name == login_name).count():
                    err['message'] = 'login_name已存在'
                    return err
            if nick_name:
                if User.query.filter(User.nick_name == nick_name).count():
                    err['message'] = 'nick_name已存在'
                    return err
            if head_picture:
                if not allowed_file_extension(head_picture.stream.filename, HEAD_PICTURE_ALLOWED_EXTENSION):
                    err['message'] = '图片的格式不支持，png jpg jpeg gif支持'
                    return err
                old_head_picture = str(user_info.base_path) + str(user_info.rel_path) + '/' + str(user_info.pic_name)
                user_info.upload_name = head_picture.stream.filename
                user_info.base_path = HEAD_PICTURE_BASE_PATH
                user_info.rel_path = HEAD_PICTURE_UPLOAD_FOLDER
                user_info.pic_name = time_file_name(secure_filename(head_picture.stream.filename), sign=user_id)
                head_picture.save(os.path.join(user_info.base_path+user_info.rel_path+'/', user_info.pic_name))
                try:
                    os.remove(old_head_picture)
                except:
                    pass
            if login_name:
                user.login_name = login_name
            if nick_name:
                user.nick_name = nick_name
            if new_password:
                user.change_password(password, new_password)
            if system_message_time:  # 1
                if not user.system_message_time:
                    user.system_message_time = todayfstr()
            else:
                user.system_message_time = None
            if mobile:
                user_info.mobile = mobile
            if tel:
                user_info.tel = tel
            if real_name:
                user_info.real_name = real_name
            if sex:
                if sex == 1 or sex == 0:
                    user_info.sex = sex
            if birthday_type:
                user_info.birthday_type = birthday_type
            if birthday:
                user_info.birthday = birthday
            if intro:
                user_info.intro = intro
            if signature:
                user_info.signature = signature
            if ethnicity_id:
                user_info.ethnicity_id = ethnicity_id
            if company:
                user_info.company = company
            if job:
                user_info.job = job
            if email:
                user_info.email = email
            if province_id:
                user_info.province_id = province_id
            if city_id:
                user_info.city_id = city_id
            if county_id:
                user_info.county_id = county_id
            if street:
                user_info.street = street

            db.add(user)
            db.add(user_info)
            db.commit()
            user = User.query.filter(User.id == user_id).first()
            user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()

            if not user_info:
                create_user_info(user.id)
                user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()
                user = User.query.filter(User.id == user_id).first()

            return wrap_user_json(user, user_info)

        if login_type == 1 or login_type == 2:
            if not open_id:
                err['message'] = '第三方登录用户必须需要open_id'
                return err
            user = User.query.filter(User.id == user_id).first()
            user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()
            if nick_name:
                if User.query.filter(User.nick_name == nick_name).count():
                    err['message'] = 'nick_name已存在'
                    return err
            if head_picture:
                if not allowed_file_extension(head_picture.stream.filename, HEAD_PICTURE_ALLOWED_EXTENSION):
                    err['message'] = '图片的格式不支持，png jpg jpeg gif支持'
                    return err
                old_head_picture = str(user_info.base_path) + str(user_info.rel_path) + '/' + str(user_info.pic_name)
                user_info.upload_name = head_picture.stream.filename
                user_info.base_path = HEAD_PICTURE_BASE_PATH
                user_info.rel_path = HEAD_PICTURE_UPLOAD_FOLDER
                user_info.pic_name = time_file_name(secure_filename(head_picture.stream.filename), sign=user_id)
                head_picture.save(os.path.join(user_info.base_path+user_info.rel_path+'/', user_info.pic_name))
                try:
                    os.remove(old_head_picture)
                except:
                    pass
            if nick_name:
                user.nick_name = nick_name
            if system_message_time:  # 1
                if not user.system_message_time:
                    user.system_message_time = todayfstr()
            else:
                user.system_message_time = None
            if mobile:
                user_info.mobile = mobile
            if tel:
                user_info.tel = tel
            if real_name:
                user_info.real_name = real_name
            if sex:
                if sex == 0 or sex == 1:
                    user_info.sex = sex
            if birthday_type:
                user_info.birthday_type = birthday_type
            if birthday:
                user_info.birthday = birthday
            if intro:
                user_info.intro = intro
            if signature:
                user_info.signature = signature
            if ethnicity_id:
                user_info.ethnicity_id = ethnicity_id
            if company:
                user_info.company = company
            if job:
                user_info.job = job
            if email:
                user_info.email = email
            if province_id:
                user_info.province_id = province_id
            if city_id:
                user_info.city_id = city_id
            if county_id:
                user_info.county_id = county_id
            if street:
                user_info.street = street

            db.add(user)
            db.add(user_info)
            db.commit()
            user = User.query.filter(User.id == user_id).first()
            user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()

            if not user_info:
                create_user_info(user.id)
                user_info = UserInfoDb.query.filter(UserInfoDb.user_id == user_id).first()
                user = User.query.filter(User.id == user_id).first()

            return wrap_user_json(user, user_info)

        return err


class UserOpenIdCheck(restful.Resource):
    """
        用户第三方登录判断
    """
    @staticmethod
    def post():
        """
            所需参数:
                1.login_type: 登录类型 0（注册用户），1（微博用户），2（QQ用户）
                2.nick_name: 用户昵称
        """
        parser = reqparse.RequestParser()
        parser.add_argument('login_type', type=str, required=True, help=u'缺少参数 login_type必须为 0（注册用户），1（微博用户），2（QQ用户）')
        parser.add_argument('open_id', type=str, required=True, help=u'缺少参数 open_id必须唯一')

        args = parser.parse_args()

        resp_suc = {}
        login_type = args['login_type']
        open_id = args['open_id']
        user = User.query.filter(User.login_type == login_type, User.open_id == open_id).first()
        if user:
            resp_suc['status'] = 0
            resp_suc['message'] = 'again'
        else:
            resp_suc['status'] = 1
            resp_suc['message'] = '填写nick_name'
        return resp_suc


def wrap_user_json(user=None, user_info=None, status=0, sign='$'):
    """将地址的ID转换为一个字符串，这里的字符串添加了一个county字段，返回一个json"""
    # db.commit()  # todo-lyw 试图修复后台注册后第一次获取不到user消息的bug，sqlalchemy和mysql的工作模式不理解，变成更大的bug了，不理解
    user_json = flatten(user)
    if user_info:
        user_info_json = flatten(user_info)
        user_info_json['county'] = get_address(user_info.province_id, user_info.city_id, user_info.county_id, sign=sign)
        if user_info.rel_path and user_info.pic_name:
            user_info_json['pic_path'] = user_info.rel_path + '/' + user_info.pic_name
        bool_to_int(user_info_json)
        return {'user':user_json, 'user_info':user_info_json, 'status':status}
        # todo-lyw 这里如果是后台注册用户，刚刚注册，然后立即获取用户消息，会额外添加一个地区的位置，为何啊
    return {'user':user_json, 'status':status}


def create_user_info(user_id):
    """通过user_id创建user_info"""
    user_info = UserInfoDb(user_id=user_id)
    db.add(user_info)
    db.commit()

def bool_to_int(json):
    """把字典的bool类型换成int的01"""
    if json['sex'] == True:
        json['sex'] = 1
    elif json['sex'] == False:
        json['sex'] = 0
    else:
        pass

def get_login_type(user_id):
    """通过用户id获取用户类型"""
    user = User.query.filter(User.id == user_id).first()

    if user:
        return user.login_type

    return None
