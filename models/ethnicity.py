# coding: utf-8

"""
    ethnicity数据库表的定义，本模块定义了Ethnicity类。
    Ethnicity类，民族信息
"""

from sqlalchemy import Column, Integer, String

from .database import Base

ETHNICITY_TABLE = 'ethnicity'


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