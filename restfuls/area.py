#coding=utf-8
#!/usr/bin/python

from flask.ext import restful
from models import Province, City
from utils.others import success_dic, fail_dic, pickler


class Area(restful.Resource):
    '''获取省市'''
    @staticmethod
    def get():
        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic

        provinces = Province.query.filter().all()
        citys = City.query.filter().all()

        resp_suc['province_list'] = []
        resp_suc['city_list'] = []
        for province in provinces:
            province_pic = pickler.flatten(province)
            resp_suc['province_list'].append(province_pic)
        for city in citys:
            city_pic = pickler.flatten(city)
            resp_suc['city_list'].append(city_pic)
        return resp_suc