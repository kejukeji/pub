# coding: UTF-8


# flask模块需要的配置参数
# ===============================================================
DEBUG = True  # 是否启动调试功能
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT^&556gh/ghj~hj/kh'  # session相关的密匙

# models模块需要的配置参数
# ===============================================================
# SQLALCHEMY_DATABASE_URI = 'mysql://root:sasa@127.0.0.1:3306/maobake_pub?charset=utf8'  # 连接的数据库
# SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/bar?charset=utf8'  # 连接的数据库
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@42.121.108.142:3306/maobake_pub?charset=utf8'  # 连接的数据库
# SQLALCHEMY_DATABASE_URI = 'mysql://root:pub12@#@61.188.37.228:3306/tour?charset=utf8'  # 连接的数据库
SQLALCHEMY_ECHO = True  # 是否显示SQL语句


# restfuls模块需要的配置参数
# ===============================================================
# 用户头像
HEAD_PICTURE_UPLOAD_FOLDER = '/static/system/head_picture'  # 运行目录的相对目录，URL获取图片的路径
HEAD_PICTURE_BASE_PATH = '/Users/X/Dropbox/Code/pub'  # pub运行文件的目录，图片的绝对路径使用
HEAD_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg', 'gif')  # 允许的拓展名
# 酒吧图片
PUB_PICTURE_UPLOAD_FOLDER = '/static/system/pub_picture'  # 运行目录的相对目录，URL获取图片的路径
PUB_PICTURE_BASE_PATH = '/Users/X/Dropbox/Code/pub'  # pub运行文件的目录，图片的绝对路径使用
PUB_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg', 'gif')  # 允许的拓展名
# 活动图片
ACTIVITY_PICTURE_UPLOAD_FOLDER = '/static/system/activity_picture'  # 运行目录的相对目录，URL获取图片的路径
ACTIVITY_PICTURE_BASE_PATH = '/Users/X/Dropbox/Code/pub'  # pub运行文件的目录，图片的绝对路径使用
ACTIVITY_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg', 'gif')  # 允许的拓展名

# 其他配置参数
# ===============================================================
# 显示调试的框框
DEBUG_TOOLBAR = True