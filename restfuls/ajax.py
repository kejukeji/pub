# coding: utf-8

"""后台管理需要的ajax文件生成"""

from flask.ext import restful
from models import PubType, Province, City, County, PubTypeMid


class GetPubType(restful.Resource):
    """获取酒吧类型字典，就是id name"""

    @staticmethod
    def get():
        pub_type = PubType.query.filter().all()

        json = []
        for i in range(len(pub_type)):
            json.append([pub_type[i].id, pub_type[i].name])

        return json


class GetProvince(restful.Resource):
    """获取省份的json"""

    @staticmethod
    def get():
        province = Province.query.filter().all()

        json = []
        for i in range(len(province)):
            json.append([province[i].id, province[i].name])

        return json


class GetCity(restful.Resource):
    """获取市的json"""

    @staticmethod
    def get(province_id):
        city = City.query.filter(City.province_id == province_id).all()

        json = []
        for i in range(len(city)):
            json.append([city[i].id, city[i].name])

        return json


class GetCounty(restful.Resource):
    """获取区县的json"""

    @staticmethod
    def get(city_id):
        county = County.query.filter(County.city_id == city_id).all()

        json = []
        for i in range(len(county)):
            json.append([county[i].id, county[i].name])

        return json


class GetPubTypeList(restful.Resource):
    """获取市的json"""

    @staticmethod
    def get(pub_id):
        pub_type = PubTypeMid.query.filter(PubTypeMid.pub_id == pub_id).all()
        type_string = ""
        for i in pub_type:
            type_string += str(i.pub_type_id)
            type_string += ','

        return [type_string.rstrip(',')]