# coding: UTF-8

from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Boolean
from database import Base
from pub import Pub
from utils import todayfstr

ACTIVITY = 'activity'


class Activity(Base):
    """
        活动
            id: 主键
            title	Varchar	标题
            pub_id	Integer	pub表相关联键
            start_date	datetime	开始时间
            end_date	datetime	结束时间
            activity_info	varchar	活动详情
            host : 0代表推荐 1代表不推荐
            join_people_number 参加人数
    """
    __tablename__ = ACTIVITY

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    activity_info = Column(String(2048), nullable=False)
    start_date = Column(DATETIME, nullable=False)
    end_date = Column(DATETIME, nullable=False)
    base_path = Column(String(100), nullable=True)
    rel_path = Column(String(100), nullable=True)
    pic_name = Column(String(100), nullable=True)
    hot = Column(Boolean, nullable=True, server_default='0')
    join_people_number = Column(Integer, nullable=True)

    def __init__(self, **kwargs):
        self.title = kwargs.pop('title')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.activity_info = kwargs.pop('activity_info')
        self.hot = kwargs.pop('hot', 0)
        self.pub_id = kwargs.pop('pub_id')
        self.join_people_number = kwargs.pop('join_people_number')

    def update(self, **kwargs):
        self.title = kwargs.pop('title')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.activity_info = kwargs.pop('activity_info')
        self.hot = kwargs.pop('hot', 0)


class ActivityPicture(Base):
    """activity_picture 对应的类
    id
    activity_id 外键 ON DELETE CASCADE ON UPDATE CASCADE
    base_path 活动图片的根路径
    rel_path 活动图片的相对路径
    pic_name 活动图片存储在服务器的名字
    upload_name 上传时候图片的名字
    """

    __tablename__ = "activity_picture"

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey(Activity.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    base_path = Column(String(128), nullable=False)
    rel_path = Column(String(128), nullable=False)
    pic_name = Column(String(128), nullable=False)
    thumbnail = Column(String(128), nullable=True, server_default=None)
    upload_name = Column(String(128), nullable=False)
    cover = Column(Boolean, nullable=False, server_default='0')

    def __init__(self, activity_id, base_path, rel_path, pic_name, upload_name, cover=0):
        self.activity_id = activity_id
        self.base_path = base_path
        self.rel_path = rel_path
        self.pic_name = pic_name
        self.upload_name = upload_name
        self.cover = cover

    def __repr__(self):
        return '<ActivityPicture(activity_id: %s, upload_name: %s)>' % (self.activity_id, self.upload_name)

    def path(self):
        return self.base_path + self.rel_path + '/'