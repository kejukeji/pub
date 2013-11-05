# coding: utf-8

from wtforms import BooleanField
from models.location import Province, City, County
import jsonpickle
import datetime


from math import sin, asin, cos, radians, fabs, sqrt, degrees

pickler = jsonpickle.pickler.Pickler(unpicklable=False, max_depth=2)


def form_to_dict(form):
    form_dict = {}

    for key in form._fields:  # 可以编写一个更好的函数，可惜我不会。。。
        if isinstance(form._fields[key].data, BooleanField) or isinstance(form._fields[key].data, int):
            form_dict[key] = form._fields[key].data
            continue

        if form._fields[key].data:
            form_dict[key] = form._fields[key].data

    return form_dict


def time_diff(dt):
    dt = datetime.datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S")
    today = datetime.datetime.today()
    s = int((today - dt).total_seconds())

    # day_diff > 365, use year
    if s / 3600 / 24 >= 365:
        return str(s / 3600 / 24 / 365) + " 年前"
    elif s / 3600 / 24 >= 30:  # day_diff > 30, use month
        return str(s / 3600 / 24 / 30) + " 个月前"
    elif s / 3600 >= 24:  # hour_diff > 24, use day
        return str(s / 3600 / 24) + " 天前"
    elif s / 60 > 60:  # minite_diff > 60, use hour
        return str(s / 3600) + " 小时前"
    elif s > 60:  # second_diff > 60, use minite
        return str(s / 60) + " 分钟前"
    else:  # use "just now"
        return "刚刚"


def page_utils(count, page, per_page=5):
    min = 1
    max = count / per_page if count % per_page == 0 else count / per_page + 1
    page = page if ( page >= min and page <= max  ) else 1

    return page, per_page


#取得一个正确的返回字典
class success_dic(object):
    def __init__(self):
        self.dic = {}
        self.dic['status'] = 0
        self.dic['message'] = 'success'
        #self.dic['test'] = 'test success'

    def set(self, k, v):
        self.dic[k] = v


#取得一个错误的返回字典
class fail_dic(object):
    def __init__(self):
        self.dic = {}
        self.dic['status'] = 1
        self.dic['message'] = '没有查询到相应数据！'
        #self.dic['test'] = 'test fail'

    def set(self, k, v):
        self.dic[k] = v


def time_to_str(time):
    """

    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_address(province_id, city_id, county_id):
    """
        参数
            province_id: 省id
            city_id: 市id
            county_id: 区id
    """
    county = County.query.filter(County.id == county_id).first()
    province = Province.query.filter(Province.id == province_id).first()
    city = City.query.filter(City.id == city_id).first()
    if province or city or county:
        return province.name + city.name + county.name
    return ''


def get_county(city_id, resp_suc):
    """
    某个区
    """
    countys = County.query.filter(County.city_id == city_id)
    if countys:
        for county in countys:
            county_pic = pickler.flatten(county)
            county_pic.pop('id')
            county_pic['area_id'] = county.id
            resp_suc['county'].append(county_pic)


EARTH_RADIUS=6371           # 地球平均半径，6371km

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance


def get_left_right_longitude_latitude(longitude, latitude):
    """

    """
    distance = get_distance_hav(12.2, 3.2, 12.3, 2.3)
    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(latitude))
    dlng = degrees(dlng)        # 弧度转换成角度


    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)     # 弧度转换成角度
    """
    left-top    : (lat + dlat, lng - dlng)
    right-top   : (lat + dlat, lng + dlng)
    left-bottom : (lat - dlat, lng - dlng)
    right-bottom: (lat - dlat, lng + dlng)
$info_sql = "select id,locateinfo,lat,lng from `lbs_info` where lat<>0 and lat>{$squares['right-bottom']['lat']} and lat<{$squares['left-top']['lat']} and lng>{$squares['left-top']['lng']} and lng<{$squares['right-bottom']['lng']} ";
sort_func = lambda park: calc_distance(lat1, lng1, park.latitude, park.longitude)
    """
