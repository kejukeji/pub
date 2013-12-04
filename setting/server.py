# coding: utf-8

from setting.secret import EX_DB_PASSWORD, EX_DB_USER, EX_SECRET_KEY_SERVER, EX_DB_NAME

# flask模块需要的配置参数
# ===============================================================
DEBUG = False  # 是否启动调试功能
SECRET_KEY = EX_SECRET_KEY_SERVER  # session相关的密匙

# models模块需要的配置参数
# ===============================================================
SQLALCHEMY_DATABASE_URI = 'mysql://' + EX_DB_USER + ':' + EX_DB_PASSWORD + '@127.0.0.1:3306/' \
                          + EX_DB_NAME + '?charset=utf8'  # 连接的数据库
SQLALCHEMY_ECHO = False  # 是否显示SQL语句

# restfuls模块需要的配置参数
# ===============================================================
# 用户头像
HEAD_PICTURE_UPLOAD_FOLDER = '/static/system/head_picture'  # 运行目录的相对目录，URL获取图片的路径
HEAD_PICTURE_BASE_PATH = '/www/pub_py'  # pub运行文件的目录，图片的绝对路径使用
HEAD_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg')  # 允许的拓展名
# 酒吧图片
PUB_PICTURE_UPLOAD_FOLDER = '/static/system/pub_picture'  # 运行目录的相对目录，URL获取图片的路径
PUB_PICTURE_BASE_PATH = '/www/pub_py'  # pub运行文件的目录，图片的绝对路径使用
PUB_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg')  # 允许的拓展名
# 活动图片
ACTIVITY_PICTURE_UPLOAD_FOLDER = '/static/system/activity_picture'  # 运行目录的相对目录，URL获取图片的路径
ACTIVITY_PICTURE_BASE_PATH = '/www/pub_py'  # pub运行文件的目录，图片的绝对路径使用
ACTIVITY_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg')  # 允许的拓展名
# 酒吧类型图片
PUB_TYPE_UPLOAD_FOLDER = '/static/pub_type_picture'
PUB_TYPE_BASE_PATH = '/www/pub_py'
PUB_TYPE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg')
# 礼物图片
GIFT_UPLOAD_FOLDER = '/static/gift_picture'
GIFT_BASE_PATH = '/www/pub_py'
GIFT_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg')

# 其他配置参数
# ===============================================================
# 显示调试的框框
DEBUG_TOOLBAR = True