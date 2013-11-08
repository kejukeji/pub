# coding: utf-8

import logging
import os

from flask.ext.admin.contrib.sqla import ModelView
from flask import flash, request
from flask.ext.admin.babel import gettext
from wtforms.fields import TextAreaField, FileField
from flask.ext import login

from models import db, Activity
from ex_var import ACTIVITY_PICTURE_BASE_PATH, ACTIVITY_PICTURE_UPLOAD_FOLDER, ACTIVITY_PICTURE_ALLOWED_EXTENSION
from utils import time_file_name, allowed_file_extension, form_to_dict
from werkzeug import secure_filename

log = logging.getLogger("flask-admin.sqla")


class ActivityView(ModelView):
    """定义活动的视图"""

    page_size = 30
    can_edit = True
    can_delete = True
    can_create = False
    column_display_pk = True
    column_searchable_list = ('title', 'activity_info')
    column_default_sort = ('start_date', True)
    column_labels = dict(
        id=u'ID',
        title=u'活动标题',
        pub_id=u'酒吧ID',
        start_date=u'活动开始时间',
        end_date=u'活动结束时间',
        hot=u'热门活动',
        activity_info=u'活动详情'
    )
    column_exclude_list = ('activity_info', 'base_path', 'rel_path', 'pic_name')

    form_overrides = dict(
        activity_info=TextAreaField
    )

    list_template = 'admin_pub/activity_list.html'
    edit_template = 'admin_pub/activity_edit.html'
    create_template = 'admin_pub/activity_create.html'

    def __init__(self, db, **kwargs):
        super(ActivityView, self).__init__(Activity, db, **kwargs)

    def scaffold_form(self):
        form_class = super(ActivityView, self).scaffold_form()
        form_class.picture = FileField(label=u'酒吧图片', description=u'原来这里可以上传酒吧图片')
        delattr(form_class, 'base_path')
        delattr(form_class, 'rel_path')
        delattr(form_class, 'pic_name')
        return form_class

    def is_accessible(self):
        return login.current_user.is_admin()

    def create_model(self, form):
        """改写flask的新建model的函数"""

        try:
            model = self.model(**form_to_dict(form))
            self.session.add(model)  # 保存酒吧基本资料
            self.session.commit()
            activity_id = model.id
            activity_pictures = request.files.getlist("picture")  # 获取酒吧图片
            save_activity_pictures(activity_id,activity_pictures)

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
            activity_id = model.id  # 获取和保存酒吧id
            activity_pictures = request.files.getlist("picture")  # 获取酒吧图片
            save_activity_pictures(activity_id, activity_pictures)
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
            delete_activity_picture(model.id)
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

def save_activity_pictures(activity_id, pictures):
    """保存酒吧图片"""
    for picture in pictures:
        if not allowed_file_extension(picture.filename, ACTIVITY_PICTURE_ALLOWED_EXTENSION):
            continue
        else:
            upload_name = picture.filename
            base_path = ACTIVITY_PICTURE_BASE_PATH
            rel_path = ACTIVITY_PICTURE_UPLOAD_FOLDER
            pic_name = time_file_name(secure_filename(upload_name), sign=activity_id)
            activity = Activity.query.filter(Activity.id == activity_id).first()
            if activity:
                old_picture = activity.base_path + activity.rel_path + '/' + activity.pic_name
                picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                activity.pic_name = pic_name
                activity.base_path = base_path
                activity.rel_path = rel_path
                db.commit()
                try:
                    os.remove(old_picture)
                except:
                    pass


def delete_activity_picture(activity_id):
    activity = Activity.query.filter(Activity.id == activity_id).first()
    if activity:
        picture = activity.base_path + activity.rel_path + '/' + activity.pic_name

        try:
            os.remove(picture)
        except:
            pass