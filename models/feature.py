# coding: utf-8

"""
    collect comment view message数据库表格对应的类
    Collect 用户收藏
    Comment 用户评论
    View 浏览的酒吧
    Message 用户私信
"""

from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from utils import todayfstr
from .pub import Pub
from .user import User
from .activity import Activity

COLLECT_TABLE = 'collect'
COMMENT_TABLE = 'comment'
VIEW_TABLE = 'view'
MESSAGE_TABLE = 'message'
FEED_BACK = 'feed_back'
ACTIVITY_COMMENT_TABLE = 'activity_comment'


class Collect(Base):
    """collect对应的类
    id
    user_id 用户ID，外键 ON DELETE CASCADE ON UPDATE CASCADE
    pub_id 酒吧ID，外键 ON DELETE CASCADE ON UPDATE CASCADE
    time 收藏时间
    """

    __tablename__ = COLLECT_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    user = relationship(User)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    pub = relationship(Pub)
    time = Column(DATETIME, nullable=False, server_default=None)

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.pub_id = kwargs.pop('pub_id')
        self.time = todayfstr()

    def __repr__(self):
        return '<Collect(user_id: %s, pub_id: %s, time: %s)>' % (self.user_id, self.pub_id, self.time)


class Comment(Base):
    """comment数据表对应的类
    id
    user_id 用户ID ON DELETE SET NULL ON UPDATE CASCADE
    pub_id 酒吧ID ON DELETE CASCADE ON UPDATE CASCADE
    time 评论时间
    content 评论内容
    star 评论给了几颗星
    """

    __tablename__ = COMMENT_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='set null', onupdate='cascade'), nullable=True)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    pub = relationship(Pub)
    time = Column(DATETIME, nullable=False, server_default=None)
    content = Column(String(256), nullable=False)
    star = Column(Integer, nullable=False, server_default='5')

    def __init__(self, user_id, pub_id, content, star=5):
        self.user_id = user_id
        self.pub_id = pub_id
        self.content = content
        self.time = todayfstr()
        self.star = star

    def __repr__(self):
        return '<Comment(user_id: %s, pub_id: %s, content: %s)>' % (self.user_id, self.pub_id, self.content)


class View(Base):
    """view对应的类
    记录用户浏览的某一个酒吧
    user_id 用户ID ON DELETE CASCADE ON UPDATE CASCADE
    pub_id 酒吧ID ON DELETE CASCADE ON UPDATE CASCADE
    time 用户最好浏览酒吧的时间
    view_number 用户一共浏览这个酒吧的次数
    """

    __tablename__ = VIEW_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    pub_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    time = Column(DATETIME, nullable=True, server_default=None)
    view_number = Column(Integer, nullable=False, server_default='0')

    def __init__(self, user_id, pub_id, view_number=0):
        self.user_id = user_id
        self.pub_id = pub_id
        self.time = todayfstr()
        self.view_number = view_number

    def __repr__(self):
        return '<View(user_id: %s, pub_id: %s)>' % (self.user_id, self.pub_id)


class Message(Base):
    """message表对应的类
    id
    sender_id 发送用户ID ON DELETE SET NULL ON UPDATE CASCADE
    receiver_id 接收用户ID ON DELETE SET NULL ON UPDATE CASCADE
    time 发送消息的时间
    content 消息的内容
    view 接收用户是否查看
    """

    __tablename__ = MESSAGE_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(User.id, ondelete='set null', onupdate='cascade'), nullable=True)
    receiver_id = Column(Integer, ForeignKey(User.id, ondelete='set null', onupdate='cascade'), nullable=True)
    content = Column(String(256), nullable=False)
    time = Column(DATETIME, nullable=True, server_default=None)
    introduction_time = Column(DATETIME, nullable=True, server_default=None)
    view = Column(Boolean, nullable=False, server_default='0')

    def __init__(self, sender_id, receiver_id, content, view=0):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.time = todayfstr()
        self.introduction_time = todayfstr()
        self.view = view

    def __repr__(self):
        return '<Message(sender_id: %s, receiver_id: %s, content: %s)>' % \
               (self.sender_id, self.receiver_id, self.content)


class FeedBack(Base):
    """
        意见反馈
            id: 主键
            content：内容
    """
    __tablename__ = FEED_BACK

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id,  ondelete='cascade', onupdate='cascade'), nullable=False)
    content = Column(String(140), nullable=True)

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.content = kwargs.pop('content')


class ActivityComment(Base):
    """comment数据表对应的类
    id
    user_id 用户ID ON DELETE SET NULL ON UPDATE CASCADE
    pub_id 酒吧ID ON DELETE CASCADE ON UPDATE CASCADE
    time 评论时间
    content 评论内容
    star 评论给了几颗星
    """

    __tablename__ = ACTIVITY_COMMENT_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='set null', onupdate='cascade'), nullable=True)
    activity_id = Column(Integer, ForeignKey(Pub.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    time = Column(DATETIME, nullable=False, server_default=None)
    content = Column(String(256), nullable=False)
    star = Column(Integer, nullable=False, server_default='5')

    def __init__(self, user_id, activity_id, content, star=5):
        self.user_id = user_id
        self.activity_id = activity_id
        self.content = content
        self.time = todayfstr()
        self.star = star