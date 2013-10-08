# coding: utf-8

"""
    统一路径管理
"""

from flask.ext.admin import Admin

from models import db
from views import UserView, UserInfoView

# 后台管理系统路径管理
admin = Admin(name=u'冒冒')
admin.add_view(UserView(db))
admin.add_view(UserInfoView(db))