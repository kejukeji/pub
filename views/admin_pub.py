# coding: utf-8

"""
    pub相关的后台代码
"""

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask.ext.login import current_user

from models import Pub, PubType, Province


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
    column_default_sort = ('recommend', False)
    column_labels = dict(
        id=u'ID',
        name=u'酒吧名',
        recommend=u'推荐',
        view_number=u'签到',
        intro=u'介绍',
        web_url=u'网址',
        mobile_list=u'移动号码列表',
        tel_list=u'固话列表',
        email=u'网址',
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
        email=u'酒吧网址',
        fax=u'酒吧的传真',
        province_id=u'省份',
        city_id=u'市，直辖市的省份和市不做区分',
        county_id=u'区县，比如上海的闵行区',
        street=u'下一级的详细地址描述',
        longitude=u'经度',
        latitude=u'纬度'
    )
    column_exclude_list = ('intro', 'web_url', 'mobile_list', 'tel_list', 'email',
                           'fax', 'street', 'longitude', 'latitude')

    form_ajax_refs = None

    def __init__(self, db, **kwargs):
        super(PubView, self).__init__(Pub, db, **kwargs)

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()