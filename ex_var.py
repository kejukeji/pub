# coding: utf-8

"""
    开发人员各自的配置数据，这是一个时常变动的文件，git文件不做管理，自己手动修改
"""

# models模块需要的配置参数
# ===============================================================
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/bar?charset=utf8'  # 连接的数据库
SQLALCHEMY_ECHO = True  # 是否显示SQL语句

# restfuls模块需要的配置参数
# ===============================================================
# 用户头像
HEAD_PICTURE_UPLOAD_FOLDER = '/upload/head_picture'  # 运行目录的相对目录，URL获取图片的路径
HEAD_PICTURE_BASE_PATH = '/Users/X/Dropbox/Code/pub'  # pub运行文件的目录，图片的绝对路径使用
HEAD_PICTURE_ALLOWED_EXTENSION = ('png', 'jpg', 'jpeg', 'gif')  # 允许的拓展名

# flask模块需要的配置参数
# ===============================================================
# 配置文件路径，测试服务器和生产服务器载入不同的配置文件
CONFIG_FILE = 'setting/lyw.cfg'

# 其他配置参数
# ===============================================================
# 显示调试的框框
DEBUG_TOOLBAR = True