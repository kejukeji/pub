# coding: utf-8

""" 项目启动的初始化文件。

项目启动的初始化文件

"""

from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.admin import Admin

from develop_vars import CONFIG_FILE

Base = declarative_base()  # 数据库ORM基础类

app = Flask(__name__)
app.config.from_pyfile(CONFIG_FILE)

admin = Admin(app)

if __name__ == "__main__":
    app.run()