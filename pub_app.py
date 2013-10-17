# coding: utf-8

""" 项目启动的初始化文件。

项目启动的初始化文件

"""

# 设置python运行环境的编码
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask
from flask.ext import restful

from models.database import db
from urls import admin
from login import login_manager, login, logout
from restfuls import UserInfo, UserLogin, UserRegister, PubGetType, PubListDetail, PubDetail, UserCollect, PubCollect,\
    PubPictureDetail, PubSearch, UserMessage
from ex_var import CONFIG_FILE

# 创建应用
app = Flask(__name__)
app.config.from_pyfile(CONFIG_FILE)

# 后台管理路径导入
admin.init_app(app)
# 用户登陆管理
login_manager.init_app(app)

# 自动关闭数据库连接
@app.teardown_appcontext
def close_db(exception=None):
    if exception is not None:
        print('++++' + str(exception) + '++++')
    db.remove()

# todo-lyw 更好的路径管理插件，直接放在这里是不知道如何放在单独文件里面
# 用户登陆相关路径
app.add_url_rule('/login', 'login', login)
app.add_url_rule('/logout', 'logout', logout)

# todo-lyw 更好的接口管理，如何放置在单独文件
# 接口文档路径管理
api = restful.Api(app)
api.add_resource(UserRegister, '/restful/user/register')
api.add_resource(UserLogin, '/restful/user/login')
api.add_resource(UserInfo, '/restful/user/user_info/<int:user_id>')
api.add_resource(PubGetType, '/restful/pub/home')
api.add_resource(PubListDetail, '/restful/pub/list/detail')
api.add_resource(PubDetail, '/restful/pub/detail')
api.add_resource(UserCollect, '/restful/user/collect')
api.add_resource(PubCollect, '/restful/pub/collect')
api.add_resource(PubPictureDetail, '/restful/pub/picture')
api.add_resource(PubSearch, '/restful/pub/search')
api.add_resource(UserMessage, '/restful/user/message')

if __name__ == '__main__':
    app.run(host='0.0.0.0')