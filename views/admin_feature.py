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
from models import Message, Collect, User, Pub
from flask.ext.admin._backwards import ObsoleteAttr


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
    column_list = ObsoleteAttr('sender_id', 'receiver_id', None)

    def __init__(self, db, **kwargs):
        super(UserMessageView, self).__init__(Message, db, **kwargs)

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


class UserCollectView(ModelView):
    """
        用户收藏
    """
    can_create = False
    can_delete = True
    can_edit = False
    column_default_sort = ('id', True)
    collects = Collect.query.filter().all()
    # user_name = []
    # pub_name = []
    #for collect in collects:
    #    user = User.query.filter(User.id == collect.user_id).first()
    #    pub = Pub.query.filter(Pub.id == collect.pub_id).first()
    #    user_name = user.nick_name
    #    pub_name = pub.name
    column_labels = dict(id=u'ID', user_id=u'用户id', pub_id=u'酒吧id', time=u'收藏时间')
    column_descriptions = dict(
        user_id=u'用户的id',
        pub_id=u'用户收藏的酒吧id'
    )
    # column_list = ObsoleteAttr(user_name, pub_name, None)

    def __init__(self, db, **kwargs):
        super(UserCollectView, self).__init__(Collect, db, **kwargs)
