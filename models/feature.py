# coding: utf-8

"""
    collect comment view message数据库表格对应的类
    Collect 用户收藏
    Comment 用户评论
    View 浏览的酒吧
    Message 用户私信
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, text
from sqlalchemy.dialects.mysql import DOUBLE

from pub_app import app, Base
from utils import time_str

COLLECT_TABLE = "collect"
COMMENT_TABLE = "comment"
VIEW_TABLE = "view"
MESSAGE_TABLE = "message"


class Collect(Base):
    """collect对应的类
    id
    user_id 用户ID，外键 ON DELETE CASCADE ON UPDATE CASCADE
    pub_id 酒吧ID，外键 ON DELETE CASCADE ON UPDATE CASCADE
    time 收藏时间
    """

    __tablename__ = COLLECT_TABLE

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='cascade', onupdate='cascade'), nullable=False)
    pub_id = Column(Integer, ForeignKey('pub.id', ondelete='cascade', onupdate='cascade'), nullable=False)
    time = Column(DATETIME, nullable=False, server_default=text('NOW()'))

    def __init__(self, user_id, pub_id, time=time_str.today()):
        self.user_id = user_id
        self.pub_id = pub_id
        self.time = time  # string '2012-02-02 02:02:02'

    def __repr__(self):
        return "<Collect(user_id: %s, pub_id: %s, time: %s)>" % (self.user_id, self.pub_id, self.time)


class Comment(Base):
    """comment数据表对应的类
    id
    user_id 用户ID ON DELETE SET NULL ON UPDATE CASCADE
    pub_id 酒吧ID ON DELETE CASCADE ON UPDATE CASCADE
    time 评论时间
    content 评论内容
    """

    __tablename__ = COMMENT_TABLE

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='set null', onupdate='cascade'), nullable=True)
    pub_id = Column(Integer, ForeignKey('pub.id', ondelete='cascade', onupdate='cascade'), nullable=False)
    time = Column(DATETIME, nullable=False, server_default=text('NOW()'))
    content = Column(String(256), nullable=False)

    def __init__(self, user_id, pub_id, content, time=time_str.today()):
        self.user_id = user_id
        self.pub_id = pub_id
        self.content = content
        self.time = time

    def __repr__(self):
        return "<Comment(user_id: %s, pub_id: %s, content: %s)>" % (self.user_id, self.pub_id, self.content)


# 运行本文件，创建数据库
if __name__ == "__main__":
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(engine)
