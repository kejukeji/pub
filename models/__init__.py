# coding: utf-8
#!/usr/bin/python -u

from models.level import Level
from models.user import User, UserInfo
from models.pub import Pub, PubType, PubPicture, PubTypeMid
from models.location import Province, City, County
from models.feature import (Collect, Comment, View, Message, FeedBack, ActivityComment,
                            Gift, UserGift, Greeting, Invitation, UserActivity)
from models.ethnicity import Ethnicity
from models.admin import SystemMessage, UserSystemMessage
from models.activity import Activity, ActivityPicture

from models.database import db
from models.database import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
