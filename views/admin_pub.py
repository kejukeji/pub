# coding: utf-8

"""
    pub相关的后台代码
"""

import logging

from flask.ext.admin.contrib.sqla import ModelView
from flask import flash
from flask.ext.admin.babel import gettext
from flask.ext.admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask.ext.login import current_user
from wtforms.fields import SelectField, StringField, BooleanField, SelectMultipleField, TextField
from wtforms import Form
from wtforms import validators
from flask.ext.admin.contrib.sqla import form
from flask.ext.admin import BaseView, expose
from flask import render_template

from models import Pub, PubType, Province
from utils import form_to_dict

log = logging.getLogger("flask-admin.sqla")


class PubTypeView(ModelView):
    """酒吧类型的类"""

    page_size = 30
    can_create = False
    can_edit = False
    can_delete = False
    column_display_pk = True
    column_searchable_list = ('name', 'code')
    column_default_sort = ('id', False)
    column_labels = dict(name=u'类型名称', code=u'类型编号', id=u'ID')
    column_descriptions = dict(
        name=u'比如：花吧',
        code=u'必须是两位，比如：01'
    )

    def __init__(self, db, **kwargs):
        super(PubTypeView, self).__init__(PubType, db, **kwargs)

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()


class PubView(ModelView):
    """定义酒吧视图"""

    page_size = 30
    can_create = True
    can_edit = True
    can_delete = True
    column_display_pk = True
    column_searchable_list = ('name',)
    column_default_sort = ('id', True)
    column_labels = dict(
        id=u'ID',
        name=u'酒吧名',
        recommend=u'推荐',
        view_number=u'签到',
        intro=u'介绍',
        web_url=u'网址',
        mobile_list=u'移动号码列表',
        tel_list=u'固话列表',
        email=u'邮箱',
        fax=u'传真',
        province_id=u'省份',
        city_id=u'市',
        county_id=u'区县',
        street=u'详细地址',
        longitude=u'经度',
        latitude=u'纬度'
    )
    column_descriptions = dict(
        id=u'ID',
        name=u'酒吧的名字',
        recommend=u'推荐酒吧',
        view_number=u'酒吧签到或者浏览酒吧的人次数',
        intro=u'酒吧基本介绍',
        web_url=u'酒吧的网站',
        mobile_list=u'酒吧的移动号码，多个号码使用英文逗号分离',
        tel_list=u'固话列表，多个号码使用英文逗号分离',
        email=u'酒吧邮箱',
        fax=u'酒吧的传真',
        province_id=u'省份',
        city_id=u'市，直辖市的省份和市不做区分',
        county_id=u'区县，比如上海的闵行区',
        street=u'下一级的详细地址描述',
        longitude=u'经度 - 填写酒吧名之后，默认搜索，点击位置方可更新',
        latitude=u'纬度 - 搜索之后，点选位置方可更新',
    )
    column_exclude_list = ('intro', 'web_url', 'mobile_list', 'tel_list', 'email',
                           'fax', 'street', 'longitude', 'latitude')

    form_ajax_refs = None

    def scaffold_form(self):
        form_class = super(PubView, self).scaffold_form()
        form_class.pub_type = TextField(label='酒吧类型', validators=[validators.input_required()],
                                        description=u'酒吧类型')
        form_class.picture = TextField(label='酒吧图片', validators=[validators.input_required()],
                                       description=u'酒吧图片，按control键可以选择多张图片')
        return form_class

    def __init__(self, db, **kwargs):
        super(PubView, self).__init__(Pub, db, **kwargs)

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

    def delete_model(self, model):
        """
            Delete model.

            :param model:
                Model to delete
        """
        try:
            self.on_model_delete(model)
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as ex:
            if self._debug:
                raise

            flash(gettext('Failed to delete model. %(error)s', error=str(ex)), 'error')
            log.exception('Failed to delete model')
            self.session.rollback()
            return False

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()