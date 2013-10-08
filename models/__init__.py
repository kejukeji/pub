# coding: utf-8

# todo-lyw 如何使用更好的包导入 pub.models.user
from models.user import User, UserInfo
from models.pub import Pub, PubType, PubPicture, PubTypeMid
from models.location import Province, City, County
from models.feature import Collect, Comment, Checkin, Message
from models.ethnicity import Ethnicity
from models.admin import SystemMessage

from models.database import db
from models.database import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # todo-lyw 一直无法理解这里为何可以创建所有的表格