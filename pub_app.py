# coding: utf-8

""" 项目启动的初始化文件。

项目启动的初始化文件

"""

from flask import Flask
from flask.ext.admin import Admin

from develop_vars import CONFIG_FILE

app = Flask(__name__)
app.config.from_pyfile(CONFIG_FILE)

admin = Admin(app, name="MM")

# 由于model.database包和pub_app包的相互包含关系这个句子只能在这里引入
from model.database import db

@app.teardown_appcontext
def close_db(exception=None):
    if exception is not None:
        print('++++' + str(exception) + '++++')
    db.remove()


if __name__ == '__main__':
    app.run()