# coding: utf-8

from wtforms import BooleanField
from models.location import Province, City, County
import jsonpickle
import datetime
import time


from math import sin, asin, cos, radians, fabs, sqrt, degrees

pickler = jsonpickle.pickler.Pickler(unpicklable=False, max_depth=2)
EARTH_RADIUS=6371           # 地球平均半径，6371km


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


#把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H")


def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False



def get_address(province_id, city_id, county_id, sign='$'):
    """
        参数
            province_id: 省id
            city_id: 市id
            county_id: 区id
    """
    county = County.query.filter(County.id == county_id).first()
    province = Province.query.filter(Province.id == province_id).first()
    city = City.query.filter(City.id == city_id).first()

    return_string = ""
    if province:
        return_string += province.name + sign
    else:
        return_string += sign
    if city:
        return_string += city.name + sign
    else:
        return_string += sign
    if county:
        return_string += county.name

    return return_string


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



#周俊的计算方法
def calc_distance( l1,  n1 ,   l2,  n2 ):
    import math
    try:
        lat1 ,longt1 ,lat2 ,longt2 = float(l1),float(n1),float(l2),float(n2)
    except:
        return (math.pi * 2 * 6371229)

    PI = math.pi # 圆周率
    R = 6371229; #地球的半径

    x = (longt2 - longt1) * PI * R * math.cos(((lat1 + lat2) / 2) * PI / 180) / 180;
    y = (lat2 - lat1) * PI * R / 180;

    distance = math.sqrt(math.pow(x, 2) + math.pow(y,2))  #两者的平方和开根号

    return distance


def get_left_right_longitude_latitude(longitude, latitude, pubs):
    """

    """
    #fr = (page-1)*page_size
    #to = page*page_size
    distance = 0.05

    ##排序后就返回fr:to
    #pubs = pubs[fr:to]
    #return pubs

    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(latitude))
    dlng = degrees(dlng)        # 弧度转换成角度

    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)     # 弧度转换成角度
    array = {'left_top': (latitude + dlat, longitude - dlng),
     'right_top': (latitude + dlat, longitude + dlng),
     'left_bottom': (latitude - dlat, longitude - dlng),
     'right_bottom': (latitude - dlat, longitude + dlng)}
    return array

