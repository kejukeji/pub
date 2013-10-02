# coding: utf-8

"""
    user与user_info数据库表的定义，本模块定义了User和UserInfo两个类。
    定义了user和user_info的ORM类。
    User: User类，主要是用户登录相关。
    UserInfo: UserInfo类，主要是用户个人信息。
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey

from pub import app, Base
from utils import time_str

USER_TABLE = "user"
USER_INFO_TABLE = "user_info"


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

    id = Column(Integer, primary_key=True)  # todo-lyw 如何实现unsigned功能
    login_name = Column(String(32), nullable=True, default=None)
    password = Column(String(64), nullable=True, default=None)  # todo-lyw password需要flask的一个插件支持
    login_type = Column(Integer, nullable=False, default=0)  # todo-lyw default无法实现，以及如何integer长度
    open_id = Column(String(64), nullable=True, default=None)
    nick_name = Column(String(32), nullable=False, unique=True)
    sign_up_date = Column(DATETIME, nullable=False)
    system_message_time = Column(DATETIME, nullable=True, default=None)
    admin = Column(Boolean, nullable=False, default=0)

    def __init__(self, login_type, nick_name, sign_up_date=time_str.today(), login_name=None, password=None,
                 open_id=None, system_message_time=time_str.today(), admin=0):
        self.login_type = login_type
        self.nick_name = nick_name
        self.sign_up_date = sign_up_date  # string "2012-09-23 23:23:23"
        self.login_name = login_name
        self.password = password
        self.open_id = open_id
        self.system_message_time = system_message_time  # string "2012-09-23 23:23:23"
        self.admin = admin

    def __repr__(self):
        return "<User(nick_name:'%s', login_type:'%s', sign_up_date:'%s')>" % (self.nick_name, self.login_type,
                                                                               self.sign_up_date)


class UserInfo(Base):
    """UserInfo类，对应数据库user_info表
    id
    user_id 用户ID 外键 ON DELETE CASCADE ON UPDATE CASCADE
    mobile 手机号 18721912400 或者 +8618721912400
    tel 固话号码 1872191 或者 07141872191
    realName 真实姓名
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
    user_id = Column(Integer, ForeignKey('user.id', ondelete="cascade", onupdate="cascade"), nullable=False)
    mobile = Column(String(16), nullable=True, default=None)
    tel = Column(String(16), nullable=True, default=None)
    realName = Column(String(32), nullable=True, default=None)
    sex = Column(Boolean, nullable=True, default=None)
    birthday_type = Column(Boolean, nullable=True, default=None)
    birthday = Column(DATETIME, nullable=True, default=None)  # string "2012-09-23 23:23:23"
    intro = Column(String(128), nullable=True, default=None)
    signature = Column(String(128), nullable=True, default=None)
    ethnicity_id = Column(Integer, nullable=True, default=None)
    company = Column(String(32), nullable=True, default=None)
    job = Column(String(32), nullable=True, default=None)
    email = Column(String(32), nullable=False)
    province_id = Column(Integer, nullable=True, default=None)
    city_id = Column(Integer, nullable=True, default=None)
    county_id = Column(Integer, nullable=True, default=None)
    street = Column(String(64), nullable=True, default=None)
    base_path = Column(String(128), nullable=True, default=None)
    rel_path = Column(String(128), nullable=True, default=None)
    pic_name = Column(String(128), nullable=True, default=None)
    upload_name = Column(String(128), nullable=True, default=None)

    def __init__(self, user_id, email, mobile=None, tel=None, real_name=None, sex=None, birthday_type=None,
                 birthday=None, intro=None, signature=None, ethnicity_id=None, company=None, job=None, province_id=None,
                 city_id=None, county_id=None, street=None, base_path=None, rel_path=None, pic_name=None,
                 upload_name=None):
        self.user_id = user_id
        self.email = email
        self.mobile = mobile
        self.tel = tel
        self.real_name = real_name
        self.sex = sex
        self.birthday_type = birthday_type
        self.birthday = birthday
        self.intro = intro
        self.signature = signature
        self.ethnicity_id = ethnicity_id
        self.company = company
        self.job = job
        self.province_id = province_id
        self.city_id = city_id
        self.county_id = county_id
        self.street = street
        self.base_path = base_path
        self.rel_path = rel_path
        self.pic_name = pic_name
        self.upload_name = upload_name

    def __repr__(self):
        return"<UserInfo(user_id:'%s', email:'%s')>" % (self.user_id, self.email)


if __name__ == "__main__":
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(engine)