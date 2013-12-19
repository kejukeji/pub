# coding: utf-8

"""
    统一路径管理
"""

import os

from flask.ext.admin import Admin
from flask.ext import restful

from pub_app import app
from models import db
from views import UserView, PubTypeView, PubView, PubFile, UserMessageView, UserCollectView, PubPictureFile
from views.admin_file import ActivityPictureFile
from views.admin_feature import UserFeedbackView
from views.admin_activity import ActivityView
from restfuls import *
from views.admin_login import login_view, logout_view, register_view
from views.admin_view import HomeView
from views.admin_system_message import SystemMessageView
from views.admin_gift import GiftView

# 用户登陆管理
# 用户登陆
app.add_url_rule('/login', 'login_view', login_view, methods=('GET', 'POST'))
app.add_url_rule('/register', 'register_view', register_view, methods=('GET', 'POST'))
app.add_url_rule('/logout', 'logout_view', logout_view, methods=('GET', 'POST'))

# 后台管理系统路径管理
admin = Admin(name=u'冒冒', index_view=HomeView())
admin.init_app(app)
admin.add_view(UserView(db, name=u'用户'))
#admin.add_view(UserMessageView(db, name=u'用户私信', category=u'功能'))
admin.add_view(UserCollectView(db, name=u'用户收藏', category=u'功能'))
admin.add_view(UserFeedbackView(db, name=u'用户反馈', category=u'功能'))

admin.add_view(PubTypeView(db, name=u'酒吧类型', category=u'酒吧'))
admin.add_view(PubView(db, name=u'酒吧详情', category=u'酒吧'))
admin.add_view(SystemMessageView(db, name=u'系统消息'))
admin.add_view(ActivityView(db, name=u'酒吧活动', category=u'酒吧'))
admin.add_view(GiftView(db, name=u'礼物管理'))

### 文件管理
file_path = os.path.join(os.path.dirname(__file__), 'static')
#admin.add_view(PubFile(file_path, '/static/', name='文件'))
pub_picture_path = os.path.join(os.path.dirname(__file__), 'static/system/pub_picture')
activity_picture_path = os.path.join(os.path.dirname(__file__), 'static/system/activity_picture')
admin.add_view(PubPictureFile(pub_picture_path, '/static/system/pub_picture/', name='酒吧图片', category=u'酒吧'))
admin.add_view(ActivityPictureFile(activity_picture_path,
                                   '/static/system/activity_picture/', name='活动图片', category=u'酒吧'))

# API接口
api = restful.Api(app)

### 后台获取相关ajax文件的路径
api.add_resource(GetPubType, '/restful/admin/pub_type')
api.add_resource(GetPubTypeList, '/restful/admin/pub_type_list/<int:pub_id>')
api.add_resource(GetProvince, '/restful/admin/province')
api.add_resource(GetCity, '/restful/admin/city/<int:province_id>')
api.add_resource(GetCounty, '/restful/admin/county/<int:city_id>')

### 接口文档路径管理
api.add_resource(UserRegister, '/restful/user/register')
api.add_resource(UserOpenIdCheck, '/restful/user/check')
api.add_resource(UserLogin, '/restful/user/login')
api.add_resource(UserInfo, '/restful/user/user_info/<int:user_id>')
api.add_resource(PubGetType, '/restful/pub/home')
api.add_resource(PubListDetail, '/restful/pub/list/detail')
api.add_resource(PubDetail, '/restful/pub/detail')
api.add_resource(UserCollect, '/restful/user/collect')
api.add_resource(PubCollect, '/restful/pub/collect')
api.add_resource(PubPictureDetail, '/restful/pub/picture')
api.add_resource(PubSearch, '/restful/pub/search')
api.add_resource(UserMessage, '/restful/user/direct/message')
api.add_resource(PubSearchView, '/restful/pub/search/view')
api.add_resource(UserMessageInfo, '/restful/user/message/info')
api.add_resource(UserSenderMessage, '/restful/user/sender/message')
api.add_resource(MessageFuck, '/restful/user/message')
api.add_resource(ClearMessage, '/restful/user/clear/message')
api.add_resource(FeedBackAdd, '/restful/feed/back')
api.add_resource(ActivityInfo, '/restful/activity/info')
#api.add_resource(CommentActivity, '/restful/activity/comment')
#api.add_resource(ActivityList, '/restful/activity/list')
# api.add_resource(ScreeningPub, '/restful/screening/county')
api.add_resource(NearPub, '/restful/near/pub')
api.add_resource(MessageByTypeInfo, '/restful/message/by/type/info')
api.add_resource(Area, '/restful/area')
api.add_resource(CancelCollectPub, '/restful/cancel/collect/pub')
api.add_resource(CollectActivity, '/restful/cancel/collect/activity')
api.add_resource(ActivityCollectList, '/restful/collect/activity/list')
api.add_resource(PersonCenter, '/restful/personal/center')
api.add_resource(CityData, '/restful/city/data')
api.add_resource(ByNameCity, '/restful/name/city')
api.add_resource(InvitationReceiver, '/restful/invitation/receiver')
api.add_resource(GreetingReceiver, '/restful/greeting/receiver')
api.add_resource(GiftReceiver, '/restful/gift/receiver')
api.add_resource(SenderInvite, '/restful/sender/invite')
api.add_resource(SenderGift, '/restful/sender/gift')
api.add_resource(SenderGiftView, '/restful/sender/gift/view')
api.add_resource(SenderGreeting, '/restful/sender/greeting')

## todo-lyw 代码末尾，形成的基本约定如下
# 文件相关的使用 static
# 接口相关的使用 restful
# 后台相关的使用 admin
# 网页相关的使用 域名！
