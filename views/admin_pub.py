# coding: utf-8

"""
    pub相关的后台代码
"""

import logging

from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin.babel import gettext
from flask import flash

from utils.form import form_to_dict
from models import Pub, PubType, PubPicture


class PubView(ModelView):
    """定义酒吧视图"""

    page_size = 30
    column_exclude_list = ('street',)
