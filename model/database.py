# coding: utf-8

"""
    定义数据库相关的内容
"""

from pub_app import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()  # 数据库ORM基础类
Base.query = db.query_property()