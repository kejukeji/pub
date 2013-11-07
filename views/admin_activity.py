# coding: utf-8

import logging
import os

from flask.ext.admin.contrib.sqla import ModelView
from flask import flash, request
from flask.ext.admin.babel import gettext
from wtforms.fields import TextField, TextAreaField
from wtforms import validators
from flask.ext import login

from models import Pub, PubType, PubTypeMid, db, PubPicture
from ex_var import PUB_PICTURE_BASE_PATH, PUB_PICTURE_UPLOAD_FOLDER, PUB_PICTURE_ALLOWED_EXTENSION
from utils import time_file_name, allowed_file_extension, form_to_dict
from werkzeug import secure_filename

from .tools import save_thumbnail
from models.activity import Activity


class ActivityView(ModelView):
    """定义活动的视图"""

    page_size = 30
    can_edit = True
    can_delete = True
    can_create = True
    column_display_pk = True
    column_searchable_list = ('title', 'activity_info')
    column_default_sort = ('start_date', True)
    column_labels = dict(
        id=u'ID',
        title=u'活动标题',
        pub_id=u'酒吧ID',
        start_date=u'活动开始时间',
        end_date=u'活动结束时间',
        hot=u'热门活动'
    )
    column_exclude_list = ('activity_info', 'base_path', 'rel_path', 'pic_name')

    list_template = 'admin_pub/activity_list.html'

    def __init__(self, db, **kwargs):
        super(ActivityView, self).__init__(Activity, db, **kwargs)

    def is_accessible(self):
        return login.current_user.is_admin()