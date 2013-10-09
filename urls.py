# coding: utf-8

"""
    统一路径管理
"""

from flask.ext.admin import Admin

from models import db
from views import UserView, PubTypeView, PubView

# 后台管理系统路径管理
admin = Admin(name=u'冒冒')
admin.add_view(UserView(db, name=u'用户'))

admin.add_view(PubTypeView(db, name=u'酒吧类型', category=u'酒吧'))
admin.add_view(PubView(db, name=u'酒吧详情', category=u'酒吧'))