# coding: utf-8

"""
    pub pub_type pub_picture数据库表的定义，本模块定义了Pub PubType PubPicture类。
    Pub: Pub类，酒吧信息。
    PubType: PubType类，酒吧类型。
    PubPicture: PubPicture类，酒吧的展示图片。
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, text
from sqlalchemy.dialects.mysql import DOUBLE

from pub_app import app, Base
from utils import time_str

PUB_TABLE = "pub"
PUB_TYPE_TABLE = "pub_type"
PUB_PICTURE_TABLE = "pub_picture"


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
    intro = Column(String(256), nullable=False, server_default=None)
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

    def __init__(self, name, type_list, longitude, latitude, province_id, city_id, county_id, street=None,
                 recommend=0, view_number=0, intro=None, web_url=None, mobile_list=None, tel_list=None,
                 email=None, fax=None):
        self.name = name
        self.type_list = type_list
        self.latitude = longitude
        self.latitude = latitude
        self.province_id = province_id
        self.city_id = city_id
        self.county_id = county_id
        self.street = self
        self.recommend = recommend
        self.view_number = view_number
        self.intro = intro
        self.web_url = web_url
        self.mobile_list = mobile_list
        self.tel_list = tel_list
        self.email = email
        self.fax = fax

    def __repr__(self):
        return "<Pub(name: '%s')>" % self.name


if __name__ == "__main__":
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(engine)