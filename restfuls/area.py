#coding=utf-8
#!/usr/bin/python

from flask.ext import restful
from models import Province, City, County
from utils.others import success_dic, fail_dic, flatten


class Area(restful.Resource):
    '''获取省市'''
    @staticmethod
    def get():
        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['list'] = []

        resp_suc = get_province_city(resp_suc)
        return resp_suc


def get_province_city(resp_suc):
    '''获取省市'''
    provinces = Province.query.filter().all()
    citys = City.query.filter().all()
    countys = County.query.filter().all()
    for province in provinces:
        province_pic = flatten(province)
        province_pic['city_list'] = []
        for city in citys:
            if city.province_id == 1 and province.id == 1:
                get_county(countys, city.id, province_pic)
            elif city.province_id == 2 and province.id == 2:
                get_county(countys, city.id, province_pic)
            elif city.province_id == 9 and province.id == 9:
                get_county(countys, city.id, province_pic)
            elif city.province_id == 22 and province.id == 22:
                get_county(countys, city.id, province_pic)
            elif city.province_id == province.id:
                city_pic = flatten(city)
                province_pic['city_list'].append(city_pic)
        resp_suc['list'].append(province_pic)
    return resp_suc

def get_county(countys,city_id, province_pic):
    '''得到直辖市的区'''
    for county in countys:
        if county.city_id == city_id:
            county_pic = flatten(county)
            province_pic['city_list'].append(county_pic)
