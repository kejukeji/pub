# coding: utf-8
#!/usr/bin/python -u

from models.user import User, UserInfo
from models.pub import Pub, PubType, PubPicture, PubTypeMid
from models.location import Province, City, County
from models.feature import Collect, Comment, View, Message, FeedBack, ActivityComment
from models.ethnicity import Ethnicity
from models.admin import SystemMessage
from models.activity import Activity

from models.database import db
from models.database import Base, engine
# todo-lyw 如何实现更好的包导入规则，init里面的导入无法事项相对路径，这个文件 <-
# -> 夹里面的包可以使用.导入不能使用..导入，这个如何处理

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # todo-lyw 一直无法理解这里为何可以创建所有的表格