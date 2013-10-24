# coding: utf-8

"""
    pub相关的后台代码
"""

import logging
import os

from flask.ext.admin.contrib.sqla import ModelView
from flask import flash, request, url_for, redirect
from flask.ext.admin.babel import gettext
from wtforms.fields import TextField
from wtforms import validators
from flask.ext.admin.base import expose
from flask.ext.admin.helpers import validate_form_on_submit
from flask.ext.admin.model.helpers import get_mdict_item_or_list

from models import Pub, PubType, PubTypeMid, db, PubPicture
from ex_var import PUB_PICTURE_BASE_PATH, PUB_PICTURE_UPLOAD_FOLDER, PUB_PICTURE_ALLOWED_EXTENSION
from utils import time_file_name, allowed_file_extension, form_to_dict
from werkzeug import secure_filename

log = logging.getLogger("flask-admin.sqla")


class PubTypeView(ModelView):
    """酒吧类型的类"""

    page_size = 30
    can_create = True
    can_edit = True
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

    edit_template = 'admin_pub/edit.html'
    create_template = 'admin_pub/create.html'

    def scaffold_form(self):
        form_class = super(PubView, self).scaffold_form()
        form_class.pub_type = TextField(label='酒吧类型', validators=[validators.input_required()],
                                        description=u'酒吧类型')
        form_class.picture = TextField(label='酒吧图片', description=u'酒吧图片，按control键可以选择多张图片')
        return form_class

    def __init__(self, db, **kwargs):
        super(PubView, self).__init__(Pub, db, **kwargs)

    def create_model(self, form):
        """改写flask的新建model的函数"""

        try:
            model = self.model(**form_to_dict(form))
            self.session.add(model)  # 保存酒吧基本资料
            self.session.commit()
            pub_id = model.id  # 获取和保存酒吧id
            pub_type_list = form.pub_type.data  # 获取酒吧的类型字符串
            pub_pictures = request.files.getlist("picture")  # 获取酒吧图片
            save_pub_type(pub_id, pub_type_list)
            save_pub_pictures(pub_id, pub_pictures)

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
            pub_id = model.id  # 获取和保存酒吧id
            pub_type_list = form.pub_type.data  # 获取酒吧的类型字符串
            pub_pictures = request.files.getlist("picture")  # 获取酒吧图片
            delete_pub_type(pub_id)
            save_pub_type(pub_id, pub_type_list)
            save_pub_pictures(pub_id, pub_pictures)
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
            delete_pub_picture(model.id)
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

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        """
            Create model view
        """
        return_url = request.args.get('url') or url_for('.index_view')

        if not self.can_create:
            return redirect(return_url)

        form = self.create_form()

        if validate_form_on_submit(form):
            if self.create_model(form):
                if '_add_another' in request.form:
                    flash(gettext('Model was successfully created.'))
                    return redirect(url_for('.create_view', url=return_url))
                else:
                    return redirect(return_url)

        return self.render(self.create_template,
                           form=form,
                           form_widget_args=self.form_widget_args,
                           return_url=return_url)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        return_url = request.args.get('url') or url_for('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        form = self.edit_form(obj=model)

        if validate_form_on_submit(form):
            if self.update_model(form, model):
                if '_continue_editing' in request.form:
                    flash(gettext('Model was successfully saved.'))
                    return redirect(request.full_path)
                else:
                    return redirect(return_url)

        return self.render(self.edit_template,
                           model=model,
                           form=form,
                           form_widget_args=self.form_widget_args,
                           return_url=return_url)

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()


def save_pub_type(pub_id, types):
    """保存酒吧类型"""

    type_list = [int(i) for i in types.split(',')]
    for pub_type in type_list:
        db.add(PubTypeMid(pub_id, pub_type))

    db.commit()


def get_pub_type(pub_id):
    """获取酒吧类型的字符串'1,2,3'"""

    pub_type = PubTypeMid.query.filter(PubTypeMid.pub_id == pub_id).all()
    type_string = ""
    for i in pub_type:
        type_string += str(i.pub_type_id)
        type_string += ','

    return type_string.rstrip(',')


def delete_pub_type(pub_id):
    """删除酒吧的类型"""
    PubTypeMid.query.filter(PubTypeMid.pub_id == pub_id).delete()


def save_pub_pictures(pub_id, pictures):
    """保存酒吧图片"""
    for picture in pictures:
        if not allowed_file_extension(picture.filename, PUB_PICTURE_ALLOWED_EXTENSION):
            continue
        else:
            upload_name = picture.filename
            base_path = PUB_PICTURE_BASE_PATH
            rel_path = PUB_PICTURE_UPLOAD_FOLDER
            pic_name = time_file_name(secure_filename(upload_name), sign=pub_id)
            db.add(PubPicture(pub_id, base_path, rel_path, pic_name, upload_name, cover=0))
            picture.save(os.path.join(base_path+rel_path+'/', pic_name))
            db.commit()


def delete_pub_picture(id):
    pictures = PubPicture.query.filter(PubPicture.pub_id == id).all()
    for picture in pictures:
        try:
            os.remove(os.path.join(picture.base_path+picture.rel_path+'/', picture.pic_name))
        except:
            pass