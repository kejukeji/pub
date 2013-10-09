# coding: utf-8

"""
    user与user_info数据库表的定义，本模块定义了User和UserInfo两个类。
    定义了user和user_info的ORM类。
    User: User类，主要是用户登录相关。
    UserInfo: UserInfo类，主要是用户个人信息。
"""

import bcrypt

from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, text

from .database import Base
from utils import todayfstr

USER_TABLE = 'user'
USER_INFO_TABLE = 'user_info'


class User(Base):
    """User类，对应于数据库的user表
    id
    login_type 用户登录类型，Integer(4)， 0表示注册用户 1表示微博登录 2表示QQ登录
    login_name 用户登录名，同一类型的登陆用户，登录名不能一样，第三方登陆用户可以为空
    password 用户密码，使用加密
    open_id 第三方登陆的openId
    nick_name 用户昵称，不可重复，第三方注册用户必须填写昵称，评论的时候使用
    sign_up_date 用户注册时间
    system_message_time 用户最后读取系统消息的时间，如果设置不读取系统消息，设置为NULL
    admin 是否具有管理员权限 0否 1是
    """

    __tablename__ = USER_TABLE

    id = Column(Integer, primary_key=True)
    login_name = Column(String(32), nullable=True, server_default=None)
    password = Column(String(64), nullable=True, server_default=None)
    login_type = Column(Integer, nullable=False, server_default='0')
    open_id = Column(String(64), nullable=True, server_default=None)
    nick_name = Column(String(32), nullable=False, unique=True)
    sign_up_date = Column(DATETIME, nullable=False, server_default=text('NOW()'))
    system_message_time = Column(DATETIME, nullable=True, server_default=text('NOW()'))
    admin = Column(Boolean, nullable=False, server_default='0')

    def __init__(self, **kwargs):
        self.login_type = kwargs.pop('login_type')
        self.nick_name = kwargs.pop('nick_name')
        self.sign_up_date = kwargs.pop('sign_up_date', todayfstr())  # string "2012-09-23 23:23:23"
        self.login_name = kwargs.pop('login_name', None)

        password = kwargs.pop('password', None)
        if password is not None:
            self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        else:
            self.password = password

        self.open_id = kwargs.pop('open_id', None)
        self.system_message_time = kwargs.pop('system_message_time', todayfstr())  # string "2012-09-23 23:23:23"
        self.admin = kwargs.pop('admin', 0)

    def __repr__(self):
        return '<User(nick_name: %s, login_type: %s, sign_up_date: %s)>' % (self.nick_name, self.login_type,
                                                                            self.sign_up_date)

    def update(self, **kwargs):
        self.login_type = kwargs.pop('login_type')
        self.nick_name = kwargs.pop('nick_name')
        self.sign_up_date = kwargs.pop('sign_up_date', todayfstr())  # string "2012-09-23 23:23:23"
        self.login_name = kwargs.pop('login_name', None)

        password = kwargs.pop('password', None)
        if password is not None:
            if self.password != password:
                self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        else:
            self.password = password

        self.open_id = kwargs.pop('open_id', None)
        self.system_message_time = kwargs.pop('system_message_time')
        self.admin = kwargs.pop('admin', 0)

    def change_password(self, old_password, new_password):
        """设置用户密码"""

        if new_password is None:
            return False

        if old_password is None:
            if self.password is None:
                self.password = bcrypt.hashpw(new_password, bcrypt.gensalt())
                return True
            else:
                return False
        else:
            if self.check_password(old_password):
                self.password = bcrypt.hashpw(new_password, bcrypt.gensalt())
                return True
            else:
                return False

    def check_password(self, password):
        """检查密码是否正确"""

        if (password is None) and (self.password is None):
            return True

        if (password is None) or (self.password is None):
            return False

        return bcrypt.checkpw(password, self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return bool(self.admin)

    def get_id(self):
        return self.id


class UserInfo(Base):
    """UserInfo类，对应数据库user_info表
    id
    user_id 用户ID 外键 ON DELETE CASCADE ON UPDATE CASCADE
    mobile 手机号 18721912400 或者 +8618721912400
    tel 固话号码 1872191 或者 07141872191
    real_name 真实姓名
    sex
    birthday_type 生日类型 0 农历 1 阳历
    birthday 出生日期
    intro 个人简介
    signature 个性签名
    ethnicity_id 民族的ID
    company 公司
    job 工作
    email 密码重置邮箱，也是用户邮箱，如果登陆名是邮箱，默认是重置邮箱
    province_id 省ID
    city_id 市ID
    county_id 区县ID
    street 地址更下一级的描述，街道门牌号等等
    base_path 头像的根目录
    rel_path 头像的相对目录
    pic_name 头像存储的文件名
    upload_name 上传时候文件名
    """

    __tablename__ = USER_INFO_TABLE

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    mobile = Column(String(16), nullable=True, server_default=None)
    tel = Column(String(16), nullable=True, server_default=None)
    real_name = Column(String(32), nullable=True, server_default=None)
    sex = Column(Boolean, nullable=True, server_default=None)
    birthday_type = Column(Boolean, nullable=True, server_default=None)
    birthday = Column(DATETIME, nullable=True, server_default=None)  # string "2012-09-23 23:23:23"
    intro = Column(String(128), nullable=True, server_default=None)
    signature = Column(String(128), nullable=True, server_default=None)
    ethnicity_id = Column(Integer, nullable=True, server_default=None)
    company = Column(String(32), nullable=True, server_default=None)
    job = Column(String(32), nullable=True, server_default=None)
    email = Column(String(32), nullable=False)
    province_id = Column(Integer, nullable=True, server_default=None)
    city_id = Column(Integer, nullable=True, server_default=None)
    county_id = Column(Integer, nullable=True, server_default=None)
    street = Column(String(64), nullable=True, server_default=None)
    base_path = Column(String(128), nullable=True, server_default=None)
    rel_path = Column(String(128), nullable=True, server_default=None)
    pic_name = Column(String(128), nullable=True, server_default=None)
    upload_name = Column(String(128), nullable=True, server_default=None)

    def __init__(self, **kwargs):  # todo-lyw这个赋值太复杂了，一定有简单的写法
        self.user_id = kwargs.pop('user_id')
        self.email = kwargs.pop('email')
        self.mobile = kwargs.pop('mobile', None)
        self.tel = kwargs.pop('tel', None)
        self.real_name = kwargs.pop('real_name', None)
        self.sex = kwargs.pop('sex', None)
        self.birthday_type = kwargs.pop('birthday_type', None)
        self.birthday = kwargs.pop('birthday', None)
        self.intro = kwargs.pop('intro', None)
        self.signature = kwargs.pop('signature', None)
        self.ethnicity_id = kwargs.pop('ethnicity_id', None)
        self.company = kwargs.pop('company', None)
        self.job = kwargs.pop('job', None)
        self.province_id = kwargs.pop('province_id', None)
        self.city_id = kwargs.pop('city_id', None)
        self.county_id = kwargs.pop('county_id', None)
        self.street = kwargs.pop('street', None)
        self.base_path = kwargs.pop('base_path', None)
        self.rel_path = kwargs.pop('rel_path', None)
        self.pic_name = kwargs.pop('pic_name', None)
        self.upload_name = kwargs.pop('upload_name', None)

    def update(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.email = kwargs.pop('email')
        self.mobile = kwargs.pop('mobile', None)
        self.tel = kwargs.pop('tel', None)
        self.real_name = kwargs.pop('real_name', None)
        self.sex = kwargs.pop('sex', None)
        self.birthday_type = kwargs.pop('birthday_type', None)
        self.birthday = kwargs.pop('birthday', None)
        self.intro = kwargs.pop('intro', None)
        self.signature = kwargs.pop('signature', None)
        self.ethnicity_id = kwargs.pop('ethnicity_id', None)
        self.company = kwargs.pop('company', None)
        self.job = kwargs.pop('job', None)
        self.province_id = kwargs.pop('province_id', None)
        self.city_id = kwargs.pop('city_id', None)
        self.county_id = kwargs.pop('county_id', None)
        self.street = kwargs.pop('street', None)
        self.base_path = kwargs.pop('base_path', None)
        self.rel_path = kwargs.pop('rel_path', None)
        self.pic_name = kwargs.pop('pic_name', None)
        self.upload_name = kwargs.pop('upload_name', None)

    def __repr__(self):
        return '<UserInfo(user_id: %s, email: %s)>' % (self.user_id, self.email)