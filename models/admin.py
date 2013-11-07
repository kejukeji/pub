# coding: utf-8

"""
    system_message表对应的类SystemMessage
"""

from sqlalchemy import Column, Integer, String, DATETIME, text, ForeignKey

from .database import Base
from .user import User
from utils import todayfstr

SYSTEM_MESSAGE_TABLE = 'system_message'
USER_SYSTEM_MESSAGE = 'user_system_message'


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
    view = Column(Integer, nullable=True, server_default=None)

    def __init__(self, **kwargs):
        self.content = kwargs.pop('content')
        self.time = todayfstr()
        self.view = 0

    def __repr__(self):
        return '<SystemMessage(content: %s, time: %s)>' % (self.content, self.time)


class UserSystemMessage(Base):
    """
       user_system_message对应的表
       id : 主键
       user_id：用户id
       system_message_id ： 系统消息id
    """
    __tablename__ = USER_SYSTEM_MESSAGE
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    system_message_id = Column(Integer, ForeignKey(SystemMessage.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    view = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.system_message_id = kwargs.pop('system_message_id')
        self.view = 0
