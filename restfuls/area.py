#coding=utf-8
#!/usr/bin/python

from flask.ext import restful
from flask.ext.restful import reqparse
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


def get_province_city_by_id(province_id, resp_suc):
    '''获取省市'''
    provinces = Province.query.filter(Province.id == province_id).first()
    citys = City.query.filter().all()
    countys = County.query.filter().all()

    province_pic = flatten(provinces)
    province_pic['city_list'] = []
    for city in citys:
        if city.province_id == 1 and provinces.id == 1:
            get_county(countys, city.id, province_pic)
        elif city.province_id == 2 and provinces.id == 2:
            get_county(countys, city.id, province_pic)
        elif city.province_id == 9 and provinces.id == 9:
            get_county(countys, city.id, province_pic)
        elif city.province_id == 22 and provinces.id == 22:
            get_county(countys, city.id, province_pic)
        elif city.province_id == provinces.id:
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


def get_city():
    '''获取城市'''
    city = City.query.filter().all()
    city_list = []
    for c in city:
        province_id = c.province_id
        if c.name == '市辖区':
            province = Province.query.filter(Province.id == c.province_id).first()
            c.name = province.name
        if c.name == '市辖县' and c.province_id != province_id:
            province = Province.query.filter(Province.id == c.province_id).first()
            c.name = province.name
        city_pic = flatten(c)
        if c.name != '市辖县' and c.name != '县':
            city_list.append(city_pic)
    return city_list


class CityData(restful.Resource):
    """
    获取城市数据
    """
    @staticmethod
    def get():
        success = success_dic().dic

        city = get_city()
        success['city'] = city

        return success


def get_province_by_name(name):
    """
    根据客户端传入一个name查找到所属省的id
    """
    city = City.query.filter(City.name.like('%'+name+'%')).first()
    province = Province.query.filter(Province.name.like('%'+name+'%')).first()
    if province:
        return province.id
    return city.province_id


class ByNameCity(restful.Resource):
    """
    通过name得到province_id返回给客户端
    """
    @staticmethod
    def get():
        """
        name: city_name 客户端穿过来的城市name
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help=u'name 必须')

        args = parser.parse_args()

        name = args['name']

        success = success_dic().dic
        fail = fail_dic().dic

        city = get_province_by_name(name)
        if city:
            success['province_id'] = city
            return success
        else:
            fail['message'] = '未查询到数据'
            return fail