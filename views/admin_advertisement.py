# coding: UTF-8

from flask.ext.admin.contrib.sqla import ModelView
from flask import request, flash
from flask.ext import login
from flask.ext.admin.babel import gettext
from wtforms.fields import FileField

import os
import Image

from utils import form_to_dict
from utils.ex_file import allowed_file_extension, time_file_name
from werkzeug import secure_filename
from models.advertisement import Advertisement
from ex_var import ADVERTISEMENT_ALLOWED_EXTENSION, ADVERTISEMENT_BASE_PATH, ADVERTISEMENT_UPLOAD_FOLDER


class AdvertisementView(ModelView):
    '''定义广告管理'''
    page_size = 30 # 页面大小。？ 不太懂。
    can_edit = True # 能否编辑
    can_delete = False # 能否删除
    can_create = True # 能否创建

    column_display_pk = True # 显示外键吗。？
    column_searchable_list = ('url',) # 根据字段搜索，可以有多个字段
    column_exclude_list = ('base_path', 'rel_path', 'picture_name') # 原来是在后台前端排除掉得字段呀
    # 标签
    column_labels = dict(
        id = u'ID',
        url = u'路径',
        upload_image = u'图片名',
        status = u'状态'
    )

    def __init__(self, db, **kwargs):
        super(AdvertisementView, self).__init__(Advertisement, db, **kwargs) # 建立model之间关联

    def scaffold_form(self):
        # 这里在干嘛，搞不懂
        form_class = super(AdvertisementView, self).scaffold_form()
        form_class.picture = FileField(label=u'广告图片', description=u'')
        # 这里不是排除掉了么，为毛还要用到
        delattr(form_class, 'base_path')
        delattr(form_class, 'rel_path')
        delattr(form_class, 'picture_name')
        delattr(form_class, 'upload_image')
        return form_class

    def is_accessible(self):
        return login.current_user.is_admin() #todo 这里应该是判断是否是管理员或者是否登录。？

    def create_model(self, form):
        '''创建model函数'''
        try:
            advertisement_pictures = request.files.getlist("picture") #todo 图片是list么不是应该获取file么
            model = self.model(**form_to_dict(form))
            if not check_save_advertisement_pictures(advertisement_pictures, model):
                return False
            self.session.add(model) # 添加到数据库中
            self.session.commit()
        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            self.session.rollback() # 如若发生异常回滚事物
            return False
        else:
            self.after_model_change(form, model, True)

        return True

    def update_model(self, form, model):
        '''更新model函数'''
        try:
            advertisement_pictures = request.files.getlist("picture") #todo 图片是list么不是应该获取file么
            model = self.model(**form_to_dict(form))
            if not check_save_advertisement_pictures(advertisement_pictures, model):
                return False
            self.session.add(model) # 添加到数据库中
            self.session.commit()
        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            self.session.rollback() # 如若发生异常回滚事物
            return False
        else:
            self.after_model_change(form, model, True)

        return True

def check_save_advertisement_pictures(advertisement_pictures, model=None, update=None):
    '''检查保存图片大小。保存'''
    for picture in advertisement_pictures:
        if (update is not None) and (model is not None): #todo 如果时修改，得到旧图片。？
            old_picture = str(model.base_path) + str(model.rel_path) + '/' + str(model.picture_name)
        if picture.filename == '': # 没图片,就不更新咯。?
            return True
        if not allowed_file_extension(picture.filename, ADVERTISEMENT_ALLOWED_EXTENSION): # 判断是否是合理图片
            flash(u'图片格式不支持， png, jpeg支持', 'error')
            return False
        upload_name = picture.filename
        base_path = ADVERTISEMENT_BASE_PATH # 得到保存广告图片绝对路径
        rel_path = ADVERTISEMENT_UPLOAD_FOLDER # 得到广告图片的相对路径
        picture_name = time_file_name(secure_filename(upload_name)) # 得到加工后图片的名字
        picture.save(os.path.join(base_path + rel_path + '/', picture_name)) # 保存图片到指定文件夹

        image = Image.open(os.path.join(base_path + rel_path + '/', picture_name)) # 得到图片
        # 这里只有先保存后才能在服务器中得到图片，所以才先保存后判断的么。？
        if image.size != (400, 100):
            flash(u'图片需要固定大小 400 * 100', 'error')
            os.remove(os.path.join(base_path + rel_path + '/', picture_name)) # 删除不合规矩的图片
            return False
        # 各个字段值赋值
        model.base_path = base_path
        model.rel_path = rel_path
        model.picture_name = picture_name

        if (update is not None) and (model is not None):
            try:
                os.remove(old_picture)
            except:
                display = "remove %s failed" % old_picture
                flash(display, 'error')

        return True