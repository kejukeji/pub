# coding: UTF-8

from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Boolean
from database import Base
from pub import Pub

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

    def __init__(self, **kwargs):
        self.title = kwargs.pop('title')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.activity_info = kwargs.pop('activity_info')
        self.hot = kwargs.pop('hot', 0)
        self.pub_id = kwargs.pop('pub_id')

    def update(self, **kwargs):
        self.title = kwargs.pop('title')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.activity_info = kwargs.pop('activity_info')
        self.hot = kwargs.pop('hot', 0)