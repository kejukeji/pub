# coding: utf-8

"""
    system_message表对应的类SystemMessage
"""

from sqlalchemy import Column, Integer, String, DATETIME, text

from .database import Base
from utils import todayfstr

SYSTEM_MESSAGE_TABLE = 'system_message'


class SystemMessage(Base):
    """system_message对应的类
    id
    content 系统消息的内容
    time 系统消息发布时间
    """

    __tablename__ = SYSTEM_MESSAGE_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    content = Column(String(128), nullable=False)
    time = Column(DATETIME, nullable=True, server_default=None)

    def __init__(self, **kwargs):
        self.content = kwargs.pop('content')
        self.time = todayfstr()

    def __repr__(self):
        return '<SystemMessage(content: %s, time: %s)>' % (self.content, self.time)
