# coding: utf-8

"""
    后台相关功能，私信，评论，等等
"""
import logging

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.babel import gettext
from flask.ext.login import current_user
from flask import flash

from utils import form_to_dict
from models import Message, Collect, User, Pub, FeedBack
from flask.ext.admin._backwards import ObsoleteAttr
from flask.ext import login


class UserMessageView(ModelView):
    """定义数据库usermessage视图"""

    page_size = 30
    can_delete = True
    can_create = False
    can_edit = False

    column_default_sort = ('id', False)
    column_searchable_list = ('content', )
    column_display_pk = True

    column_labels = dict(id=u'ID', sender_id=u'发送用户id', receiver_id=u'接受用户id', time=u'发送时间',
                         content=u'发送内容')
    column_descriptions = dict(
        sender_id=u'发送用户id',
        receiver_id=u'接受用户id',
        time=u'发送时间',
        content=u'发送的内容'
    )

    def __init__(self, db, **kwargs):
        super(UserMessageView, self).__init__(Message, db, **kwargs)

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()

    def is_accessible(self):
        return login.current_user.is_admin()

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


class UserCollectView(ModelView):
    """
        用户收藏
    """
    can_create = False
    can_delete = True
    can_edit = False
    column_labels = {
        'id': u'ID',
        'user.nick_name': u'用户昵称',
        'pub.name': u'酒吧',
        'time': u'收藏时间'
    }

    column_list = ('id', 'user.nick_name', 'pub.name', 'time')

    def __init__(self, db, **kwargs):
        super(UserCollectView, self).__init__(Collect, db, **kwargs)

    def is_accessible(self):
        return login.current_user.is_admin()


class UserFeedbackView(ModelView):
    """
        用户收藏
    """
    can_create = False
    can_delete = True
    can_edit = False
    column_labels = {
        'id': u'ID',
        'user.nick_name': u'用户昵称',
        'content': u'内容',
        'time': u'时间'
    }

    column_list = ('id', 'user.nick_name', 'content', 'time')

    def __init__(self, db, **kwargs):
        super(UserFeedbackView, self).__init__(FeedBack, db, **kwargs)

    def is_accessible(self):
        return login.current_user.is_admin()
