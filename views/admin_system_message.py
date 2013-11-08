# coding: utf-8

import logging

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.babel import gettext
from flask.ext import login
from flask import flash
from wtforms import TextAreaField

from utils import form_to_dict
from models import SystemMessage


class SystemMessageView(ModelView):
    """定义了系统消息的视图"""

    page_size = 30
    can_delete = True
    can_edit = True
    can_create = True
    column_searchable_list = ('content',)
    column_default_sort = ('time', True)
    column_exclude_list = ('view',)
    column_display_pk = True
    column_labels = dict(
        id=u'ID',
        content=u'消息内容',
        time=u'时间'
    )
    form_overrides = dict(
        content=TextAreaField
    )


    def __init__(self, db, **kwargs):
        super(SystemMessageView, self).__init__(SystemMessage, db, **kwargs)

    def is_accessible(self):
        return login.current_user.is_admin()

    def scaffold_form(self):
        form_class = super(SystemMessageView, self).scaffold_form()
        delattr(form_class, 'time')
        delattr(form_class, 'view')
        return form_class

    def create_model(self, form):
        """改写flask的新建model的函数"""

        try:
            model = self.model(**form_to_dict(form))
            self.session.add(model)  # 保存酒吧基本资料
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