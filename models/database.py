# coding: utf-8

"""
    数据库相关的变量
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from develop_vars import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=SQLALCHEMY_ECHO)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db.query_property()