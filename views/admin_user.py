# coding: utf-8

"""
    user相关的后台代码
"""

import logging

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.babel import gettext
from flask.ext.login import current_user
from flask import flash

from utils import form_to_dict
from models import User


class UserView(ModelView):
    """定义数据库user视图"""

    page_size = 30
    can_delete = False
    column_exclude_list = ('password', 'open_id')
    column_default_sort = ('sign_up_date', True)
    column_searchable_list = ('login_name', 'nick_name')
    column_display_pk = True
    column_choices = {
        'login_type': [
            (0, u'注册用户'),
            (1, u'微博用户'),
            (2, u'QQ用户')
        ]
    }
    column_labels = dict(id=u'ID', login_name=u'登录名', password=u'密码', login_type=u'登陆类型', nick_name=u'昵称',
                         open_id=u'第三方登陆ID', sign_up_date=u'注册时间', system_message_time=u'系统消息',
                         admin=u'管理员')
    column_descriptions = dict(
        system_message_time=u'最后接收系统消息的时间，如果没有显示时间，表示用户禁止接收系统消息',
        admin=u'用户是否具有管理员权限',
        login_type=u'注册用户和第三方登录',
        login_name=u'登录名，用户用于登录应用的名称，可以是邮箱或者是手机号',
        nick_name=u'用户昵称，比如用户评论，显示的是用户昵称，而不是邮箱或者手机号'
    )

    def __init__(self, db, **kwargs):
        super(UserView, self).__init__(User, db, **kwargs)

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()

    def create_model(self, form):
        """改写flask的新建model的函数"""

        try:
            model = self.model(**form_to_dict(form))
            self.session.add(model)
            self.session.commit()
        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to create model')
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)

        return True

    def update_model(self, form, model):
        """改写了update函数"""
        try:
            model.update(**form_to_dict(form))
            self.session.commit()
        except Exception, ex:
            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to update model')
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, False)

        return True