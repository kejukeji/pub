# coding: UTF-8

from sqlalchemy import String, Integer, Column
from .database import Base


ADVERTISEMENTS = 'advertisement'

class Advertisement(Base):
    """
    广告
    id 自增咧
    url 广告指向地址
    base_path 绝对路劲
    rel_path 相对路劲
    picture_name 图片名
    upload_image 文件名
    status 状态
    """
    __tablename__ = ADVERTISEMENTS

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=True, server_default='')
    base_path = Column(String(100), nullable=True, default='/www/pub')
    rel_path = Column(String(100), nullable=True, default='/static/system/advertisement_picture')
    picture_name = Column(String(100), nullable=True, default='picture')
    upload_image = Column(String(100), nullable=True, default='upload')
    status = Column(String(2), nullable=True)

    def __init__(self, **kwargs):
        self.url = kwargs.pop('url')
        self.status = kwargs.pop('status')


def get_advertisement_by_id(advertisement_id):
    '''通过id得到广告'''
    advertisement = Advertisement.query.filter(Advertisement.id == advertisement_id).first()
    return advertisement