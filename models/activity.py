# coding: UTF-8

from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
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
    """
    __tablename__ = ACTIVITY
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='set null', onupdate='cascade'), nullable=True)
    activity_info = Column(String(500), nullable=True)
    start_date = Column(DATETIME, nullable=True)
    end_date = Column(DATETIME, nullable=True)
    base_path = Column(String(100), nullable=True)
    rel_path = Column(String(100), nullable=True)
    pic_name = Column(String(100), nullable=True)

    def __init__(self, **kwargs):
        self.title = kwargs.pop('title')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.activity_info = kwargs.pop('activity_info')