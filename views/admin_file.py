# coding: utf-8

from flask.ext.admin.contrib.fileadmin import FileAdmin


class PubFile(FileAdmin):
    """酒吧后台文件管理"""

    can_upload = True
    can_delete = True
    can_delete_dirs = False
    can_mkdir = True
    can_rename = False


class PubPicture(FileAdmin):
    """酒吧图片的后台管理"""
    pass