# coding: utf-8

"""
    ethnicity数据库表的定义，本模块定义了Ethnicity类。
    Ethnicity类，民族信息
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

ETHNICITY_TABLE = 'ethnicity'

Base = declarative_base()


class Ethnicity(Base):
    """ethnicity表对应的类
    id
    name 民族名
    code 标志位
    """

    __tablename__ = ETHNICITY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    code = Column(String(4), nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return '<Ethnicity(name: %s)>' % self.name


# 运行本文件，创建数据库
if __name__ == '__main__':
    from pub_app import engine
    Base.metadata.create_all(engine)