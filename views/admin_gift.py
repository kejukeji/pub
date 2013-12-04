# coding: utf-8

from flask.ext.admin.contrib.sqla import ModelView
from flask import flash, request
from wtforms.fields import FileField, TextField
from flask.ext import login
from flask.ext.admin.babel import gettext
import logging
import os
import Image

from models import Gift
from utils import form_to_dict
from utils.ex_file import allowed_file_extension, time_file_name
from werkzeug import secure_filename
from ex_var import GIFT_ALLOWED_EXTENSION, GIFT_BASE_PATH, GIFT_UPLOAD_FOLDER

log = logging.getLogger("flask-admin.sqla")


class GiftView(ModelView):
    """定义礼物管理视图"""

    page_size = 30
    can_edit = True
    can_delete = False
    can_create = True
    column_display_pk = True
    column_searchable_list = ('name',)
    column_exclude_list = ('base_path', 'rel_path', 'pic_name')
    column_labels = dict(
        id=u'ID',
        status=u'运营',
        words=u'祝福',
        name=u'名称',
        cost=u'所需积分'
    )

    def __init__(self, db, **kwargs):
        super(GiftView, self).__init__(Gift, db, **kwargs)

    def scaffold_form(self):
        form_class = super(GiftView, self).scaffold_form()
        form_class.picture = FileField(label=u'礼物图片', description=u'礼物图片，要有爱哦')
        delattr(form_class, 'base_path')
        delattr(form_class, 'rel_path')
        delattr(form_class, 'pic_name')
        return form_class

    def is_accessible(self):
        return login.current_user.is_admin()

    def create_model(self, form):
        """改写flask的新建model的函数"""

        try:
            gift_pictures = request.files.getlist("picture")
            model = self.model(**form_to_dict(form))
            if not check_save_gift_pictures(gift_pictures, model):
                return False  # 保存图片， 同时更新model的路径消息，不删除历史图片
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
            gift_pictures = request.files.getlist("picture")
            model.update(**form_to_dict(form))
            if not check_save_gift_pictures(gift_pictures, model, update=1):
                return False  # 保存图片， 同时更新model的路径消息，不删除历史图片
            self.session.commit()
        except Exception, ex:
            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to update model')
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, False)

        return True


def check_save_gift_pictures(gift_pictures, model=None, update=None):
    """200*200的图片"""

    for picture in gift_pictures:
        if (update is not None) and (model is not None):
            old_picture = str(model.base_path) + str(model.rel_path) + '/' + str(model.pic_name)
        if picture.filename == '':  # 或许没有图片，那么图片不更新
            return True
        if not allowed_file_extension(picture.filename, GIFT_ALLOWED_EXTENSION):
            flash(u'图片格式不支持啊，png，jpeg支持', 'error')
            return False
        upload_name = picture.filename
        base_path = GIFT_BASE_PATH
        rel_path = GIFT_UPLOAD_FOLDER
        pic_name = time_file_name(secure_filename(upload_name))
        picture.save(os.path.join(base_path+rel_path+'/', pic_name))

        image = Image.open(os.path.join(base_path+rel_path+'/', pic_name))

        if image.size != (200, 200):
            flash(u'图片需要固定大小的哦 200 * 200', 'error')
            os.remove(os.path.join(base_path+rel_path+'/', pic_name))
            return False

        model.base_path = base_path
        model.rel_path = rel_path
        model.pic_name = pic_name

        if (update is not None) and (model is not None):
            try:
                os.remove(old_picture)
            except:
                display = "remove %s failed" % old_picture
                flash(display, 'error')

        return True
