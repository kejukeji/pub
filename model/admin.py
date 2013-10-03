# coding: utf-8

"""
    system_message表对应的类SystemMessage
"""

from sqlalchemy import Column, Integer, String, DATETIME, text
from sqlalchemy.ext.declarative import declarative_base

from utils import time_str

SYSTEM_MESSAGE_TABLE = 'system_message'

Base = declarative_base()


class SystemMessage(Base):
    """system_message对应的类
    id
    content 系统消息的内容
    time 系统消息发布时间
    """

    __tablename__ = SYSTEM_MESSAGE_TABLE

    id = Column(Integer, primary_key=True)
    content = Column(String(128), nullable=False)
    time = Column(DATETIME, nullable=False, server_default=text('NOW()'))

    def __init__(self, content, time=time_str.today()):
        self.content = content
        self.time = time

    def __repr__(self):
        return '<SystemMessage(content: %s, time: %s)>' % (self.content, self.time)


# 运行本文件，创建数据库
if __name__ == '__main__':
    from pub_app import engine
    Base.metadata.create_all(engine)
