# coding: utf-8

""" 项目启动的初始化文件。

项目启动的初始化文件

"""

# 设置python运行环境的编码
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask

from models.database import db
from urls import admin
from develop_vars import CONFIG_FILE

# 创建应用
app = Flask(__name__)
app.config.from_pyfile(CONFIG_FILE)

# 后台管理路径导入
admin.init_app(app)

# 自动关闭数据库连接
@app.teardown_appcontext
def close_db(exception=None):
    if exception is not None:
        print('++++' + str(exception) + '++++')
    db.remove()


if __name__ == '__main__':
    app.run()