# coding: utf-8

"""
    pub pub_type pub_picture数据库表的定义，本模块定义了Pub PubType PubPicture类。
    Pub: Pub类，酒吧信息。
    PubType: PubType类，酒吧类型。
    PubPicture: PubPicture类，酒吧的展示图片。
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE

from .database import Base

PUB_TABLE = 'pub'
PUB_TYPE_TABLE = 'pub_type'
PUB_PICTURE_TABLE = 'pub_picture'
PUB_TYPE_MID_TABLE = 'pub_type_mid'


class Pub(Base):
    """Pub类，数据库的pub表
    id
    name 酒吧名称
    recommend 是否为推荐酒吧 0 不是 1 是
    type_list 酒吧类型列表，英文逗号分离，必须为两位一个 01,02,03
    view_number 浏览酒吧的人数，一人一天最多只能一次
    intro 酒吧介绍
    web_url 酒吧的网站
    mobile_list 酒吧的固话列表，使用英文逗号分离
    tel_list 酒吧的移动号码列表，使用英文逗号分离
    email 酒吧邮箱
    fax 酒吧传真
    province_id 省ID
    city_id 市ID
    county_id 区县ID
    street 更下一级的地址描述
    longitude 经度
    latitude 纬度
    """

    __tablename__ = PUB_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    recommend = Column(Boolean, nullable=False, server_default='0')
    view_number = Column(Integer, nullable=False, server_default='0')
    intro = Column(String(2048), nullable=False)
    web_url = Column(String(64), nullable=True, server_default=None)
    mobile_list = Column(String(128), nullable=True, server_default=None)
    tel_list = Column(String(128), nullable=True, server_default=None)
    email = Column(String(32), nullable=True, server_default=None)
    fax = Column(String(16), nullable=True, server_default=None)
    province_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    county_id = Column(Integer, nullable=False)
    street = Column(String(64), nullable=True, server_default=None)
    longitude = Column(DOUBLE, nullable=False)
    latitude = Column(DOUBLE, nullable=False)
    stopped = Column(Boolean, nullable=False, server_default='0')

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.longitude = kwargs.pop('longitude')
        self.latitude = kwargs.pop('latitude')
        self.province_id = kwargs.pop('province_id')
        self.city_id = kwargs.pop('city_id')
        self.county_id = kwargs.pop('county_id')
        self.stopped = kwargs.pop('stopped')
        self.street = kwargs.pop('street', None)
        self.recommend = kwargs.pop('recommend', 0)
        self.view_number = kwargs.pop('view_number', 0)
        self.intro = kwargs.pop('intro', None)
        self.web_url = kwargs.pop('web_url', None)
        self.mobile_list = kwargs.pop('mobile_list', None)
        self.tel_list = kwargs.pop('tel_list', None)
        self.email = kwargs.pop('email', None)
        self.fax = kwargs.pop('fax', None)

    def update(self, **kwargs):
        self.name = kwargs.pop('name')
        self.longitude = kwargs.pop('longitude')
        self.latitude = kwargs.pop('latitude')
        self.province_id = kwargs.pop('province_id')
        self.city_id = kwargs.pop('city_id')
        self.county_id = kwargs.pop('county_id')
        self.stopped = kwargs.pop('stopped')
        self.street = kwargs.pop('street', None)
        self.recommend = kwargs.pop('recommend', 0)
        self.view_number = kwargs.pop('view_number', 0)
        self.intro = kwargs.pop('intro', None)
        self.web_url = kwargs.pop('web_url', None)
        self.mobile_list = kwargs.pop('mobile_list', None)
        self.tel_list = kwargs.pop('tel_list', None)
        self.email = kwargs.pop('email', None)
        self.fax = kwargs.pop('fax', None)

    def __repr__(self):
        return '<Pub(name: %s)>' % self.name


class PubType(Base):
    """pub_type相对于的PubType类
    id
    name 酒吧类型
    code 标志位
    """

    __tablename__ = PUB_TYPE_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    code = Column(String(4), nullable=False)
    base_path = Column(String(100), nullable=True)
    rel_path = Column(String(100), nullable=True)
    pic_name = Column(String(100), nullable=True)

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.code = kwargs.pop('code')

    def update(self, **kwargs):
        self.name = kwargs.pop('name')
        self.code = kwargs.pop('code')

    def __repr__(self):
        return '<PubType(name: %s, code: %s)>' % (self.name, self.code)


class PubPicture(Base):
    """pub_picture 对应的类
    id
    pub_id 外键 ON DELETE CASCADE ON UPDATE CASCADE
    base_path 酒吧图片的根路径
    rel_path 酒吧图片的相对路径
    pic_name 酒吧图片存储在服务器的名字
    upload_name 上传时候图片的名字
    """

    __tablename__ = PUB_PICTURE_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    base_path = Column(String(128), nullable=False)
    rel_path = Column(String(128), nullable=False)
    pic_name = Column(String(128), nullable=False)
    thumbnail = Column(String(128), nullable=True, server_default=None)
    upload_name = Column(String(128), nullable=False)
    cover = Column(Boolean, nullable=False, server_default='0')

    def __init__(self, pub_id, base_path, rel_path, pic_name, upload_name, cover=0):
        self.pub_id = pub_id
        self.base_path = base_path
        self.rel_path = rel_path
        self.pic_name = pic_name
        self.upload_name = upload_name
        self.cover = cover

    def __repr__(self):
        return '<PubPicture(pub_id: %s, upload_name: %s)>' % (self.pub_id, self.upload_name)

    def path(self):
        return self.base_path + self.rel_path + '/'


class PubTypeMid(Base):
    """pub_type_mid 对应的类
    id
    pub_id 外键 ON DELETE CASCADE ON UPDATE CASCADE
    pub_type_id 外键 ON DELETE CASCADE ON UPDATE CASCADE
    """

    __tablename__ = PUB_TYPE_MID_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    pub_type_id = Column(Integer, ForeignKey(PubType.id, ondelete='cascade', onupdate='cascade'), nullable=False)

    def __init__(self, pub_id, pub_type_id):
        self.pub_id = pub_id
        self.pub_type_id = pub_type_id

    def __repr__(self):
        return '<PubTypeMid(pub_id: %s, pub_type_id: %s)>' % (self.pub_id, self.pub_type_id)