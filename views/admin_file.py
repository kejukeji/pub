# coding: utf-8

from flask.ext.admin.contrib.fileadmin import FileAdmin


class PubFile(FileAdmin):
    """酒吧后台文件管理"""

    can_upload = False
    can_delete = False
    can_delete_dirs = False
    can_mkdir = False
    can_rename = False