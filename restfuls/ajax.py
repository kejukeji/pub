# coding: utf-8

"""后台管理需要的ajax文件生成"""

from flask.ext import restful
from models import PubType


class GetPubType(restful.Resource):
    """获取酒吧类型字典，就是id name"""

    @staticmethod
    def get():
        pub_type = PubType.query.filter().all()

        json = {}
        for i in range(len(pub_type)):
            json[i] = pub_type[i].name

        return json