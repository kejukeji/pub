# coding: utf-8
from sqlalchemy import Column, Integer, String, desc
from models.database import Base


class Level(Base):
    """经验值对应的等级
    id
    min  等级区间的最低经验值
    max  等级区间的最高经验值
    short_name  等级名 LV1
    long_name   等级别名 泡吧至尊
    """

    __tablename__ = 'level'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)
    short_name = Column(String(8), nullable=False)
    long_name = Column(String(16), nullable=False)
    level = Column(Integer, nullable=False, server_default="1")

    def __init__(self, **kwargs):
        self.min = kwargs.pop('min')
        self.max = kwargs.pop('max')
        self.short_name = kwargs.pop('short_name')
        self.long_name = kwargs.pop('long_name')
        self.level = kwargs.pop("level", 1)


def get_level(number):
    """通过经验值获取当前的级别 (1, "LV.1", "LOL王者")"""
    level_desc = Level.query.filter(Level.min < number).order_by(desc(Level.level)).first()
    return int(level_desc.level), str(level_desc.short_name), str(level_desc.long_name)