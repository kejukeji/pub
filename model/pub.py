# coding: utf-8

"""
    pub pub_type pub_picture数据库表的定义，本模块定义了Pub PubType PubPicture类。
    Pub: Pub类，酒吧信息。
    PubType: PubType类，酒吧类型。
    PubPicture: PubPicture类，酒吧的展示图片。
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base

PUB_TABLE = 'pub'
PUB_TYPE_TABLE = 'pub_type'
PUB_PICTURE_TABLE = 'pub_picture'

Base = declarative_base()


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

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    recommend = Column(Boolean, nullable=False, server_default='0')
    type_list = Column(String(32), nullable=False)
    view_number = Column(Integer, nullable=False, server_default='0')
    intro = Column(String(256), nullable=False)
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

    def __init__(self, name, type_list, longitude, latitude, province_id, city_id, county_id, **kwargs):
        self.name = name
        self.type_list = type_list
        self.latitude = longitude
        self.latitude = latitude
        self.province_id = province_id
        self.city_id = city_id
        self.county_id = county_id
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

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    code = Column(String(4), nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

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

    id = Column(Integer, primary_key=True)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    base_path = Column(String(128), nullable=False)
    rel_path = Column(String(128), nullable=False)
    pic_name = Column(String(128), nullable=False)
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


# 运行本文件，创建数据库
if __name__ == '__main__':
    from pub_app import engine
    Base.metadata.create_all(engine)