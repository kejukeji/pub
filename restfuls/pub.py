#coding=utf-8
#!/usr/bin/python

from flask.ext import restful
from models import Pub, PubType, PubTypeMid, PubPicture, engine, View, UserInfo, User, db, Activity,\
    ActivityComment, Collect
from utils import pickler, page_utils
from flask.ext.restful import reqparse
from utils.others import success_dic, fail_dic, get_address, get_county, flatten, max_page


def to_flatten(obj, obj2):
    """
    转换json对象
    """
    obj_pic = None
    if obj:
        obj_pic = flatten(obj)
    if obj2:
        if obj2.rel_path and obj2.thumbnail:
            obj_pic['pic_path'] = obj2.rel_path + '/' + obj2.thumbnail
    return obj_pic


def to_pub_longitude_latitude(pub, picture):
    """
        经度纬度
        def calc_distance( l1,  n1 ,   l2,  n2 ):
            import math
            lat1 ,longt1 ,lat2 ,longt2 = float(l1),float(n1),float(l2),float(n2)

            PI = math.pi # 圆周率
            R = 6371229; #地球的半径

            x = (longt2 - longt1) * PI * R * math.cos(((lat1 + lat2) / 2) * PI / 180) / 180;
            y = (lat2 - lat1) * PI * R / 180;

            distance = math.sqrt(math.pow(x, 2) + math.pow(y,2))  #两者的平方和开根号

            return distance
    """
    pub_pic = flatten(pub)
    if picture:
        if picture.rel_path and picture.thumbnail:
            pub_pic['pic_path'] = picture.rel_path + '/' + picture.thumbnail
    pub_pic.pop('longitude')
    pub_pic.pop('latitude')
    pub_pic['longitude'] = str(pub.longitude)
    pub_pic['latitude'] = str(pub.latitude)
    return pub_pic


def to_city(obj_pic, county):
    """
        所在城市
    """
    if county:
        obj_pic['city_county'] = county.name


def to_pub_type(pub, obj_pic):
    """
        遍历一个酒吧对应多个类型和对应一个类型
    """
    if pub:
        obj_pic['type_name'] = ''
        ptm_count = PubTypeMid.query.filter(PubTypeMid.pub_id == pub.id).count()
        if ptm_count > 1:
            pub_type_mids = PubTypeMid.query.filter(PubTypeMid.pub_id == pub.id).all()
            for pub_type in pub_type_mids:
                p_type = PubType.query.filter(PubType.id == pub_type.pub_type_id).first()
                obj_pic['type_name'] = obj_pic['type_name'] + '/' + p_type.name
        else:
            pub_type = PubTypeMid.query.filter(PubTypeMid.pub_id == pub.id).first()
            p_type = PubType.query.filter(PubType.id == pub_type.pub_type_id).first()
            obj_pic['type_name'] = p_type.name

#
#
# def to_pub_type_only(pub_type, obj_pic):
#     """
#         遍历一个酒吧对应一个类型
#     """
#     if pub_type:
#         p_type = PubType.query.filter(PubType.id == pub_type.pub_type_id).first()
#         obj_pic['type_name'] = p_type.name


def pub_list_picture(pub_pictures, resp_suc):
    """
    遍历多个酒吧图片
    """
    for pub_picture in pub_pictures:
        pub_picture_pic = to_flatten(pub_picture, pub_picture)
        pub = Pub.query.filter(Pub.id == pub_picture.pub_id).first()
        change_latitude_longitude(pub_picture_pic, pub)
        picture_pub(pub_picture_pic, pub, pub_picture)
        resp_suc['county'] = get_address(pub.province_id, pub.city_id, pub.county_id)
        resp_suc['picture_list'].append(pub_picture_pic)


def user_list_picture(pub_pictures, resp_suc):
    """
        遍历多个用户图片
    """
    for pub_picture in pub_pictures:
        pub_picture_pic = to_flatten(pub_picture, pub_picture)
        resp_suc['picture_list'].append(pub_picture_pic)


def user_picture_only(pub_picture, resp_suc):
    """
        单个用户图片
    """
    if pub_picture:
        pub_picture_pic = to_flatten(pub_picture, pub_picture)
        resp_suc['picture_list'].append(pub_picture_pic)


def pub_picture_only(pub_picture, resp_suc):
    """
        单个酒吧图片
    """
    if pub_picture:

        pub_picture_pic = to_flatten(pub_picture, pub_picture)
        pub = Pub.query.filter(Pub.id == pub_picture.pub_id).first()
        change_latitude_longitude(pub_picture_pic, pub)
        picture_pub(pub_picture_pic, pub, pub_picture)
        resp_suc['county'] = get_address(pub.province_id, pub.city_id, pub.county_id)
        resp_suc['picture_list'].append(pub_picture_pic)


def picture_pub(pub_picture_pic, pub, pub_picture):
    """
        酒吧图片，添加酒吧信息
    """
    pub_picture_pic.pop('id')
    pub_picture_pic.pop('pub_id')
    pub_picture_pic['name'] = pub.name
    pub_picture_pic['id'] = pub_picture.pub_id
    pub_picture_pic['intro'] = pub.intro
    pub_picture_pic['view_number'] = pub.view_number
    to_pub_type(pub, pub_picture_pic)


def pub_list(pubs, resp_suc):
    """
        遍历多个酒吧
    """
    for pub in pubs:
        pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub.id).first()
        pub_pic = to_flatten(pub, pub_picture)
        pub_pic.pop('longitude')
        pub_pic.pop('latitude')
        resp_suc['county'] = get_address(pub.province_id, pub.city_id, pub.county_id)
        change_latitude_longitude(pub_pic, pub)
        resp_suc['pub_list'].append(pub_pic)


def pub_only(pub, resp_suc):
    """
        一个酒吧
    """
    if pub:
        pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub.id).first()
        pub_pic = to_flatten(pub, pub_picture)
        pub_pic.pop('longitude')
        pub_pic.pop('latitude')
        pub_pic.pop('county_id')
        pub_pic['area'] = get_address(pub.province_id, pub.city_id, pub.county_id)
        to_pub_type(pub, pub_pic)
        change_latitude_longitude(pub_pic, pub)
        resp_suc['pub_list'].append(pub_pic)


def pub_activity(activity):
    """
        活动的关联酒吧
    """
    activity_pic = to_flatten(activity, activity)
    pub = Pub.query.filter(Pub.id == activity.pub_id).first()

    activity_pic['picture_path'] = ''
    activity_pic['pub_name'] = ''
    if activity.rel_path and activity.pic_name:
        activity_pic['activity_picture_path'] = activity.rel_path + '/' + activity.pic_name
    if pub:
        pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub.id).first()
        if pub_picture.rel_path and pub_picture.thumbnail:
            activity_pic['pub_picture_path'] = pub_picture.rel_path + '/' + pub_picture.thumbnail
        activity_pic['pub_name'] = pub.name
    activity_pic['county'] = get_address(pub.province_id, pub.city_id, pub.county_id)
    return activity_pic


def comment_user(count, activity, resp_suc):
    """
        评论内容以及用户信息
    """
    if count > 1:
        activity_comments = ActivityComment.query.filter(ActivityComment.activity_id == activity.id)
        for activity_comment in activity_comments:
            activity_pic = to_flatten(activity_comment, None)
            user_info(activity_comment, activity_pic)
            resp_suc['comment_list'].append(activity_pic)
    else:
        activity_comment = ActivityComment.query.filter(ActivityComment.activity_id == activity.id).first()
        activity_pic = to_flatten(activity_comment, None)
        user_info(activity_comment, activity_pic)
        resp_suc['comment_list'].append(activity_pic)


def user_info(activity_comment, pic):
    """

    """
    user = User.query.filter(User.id == activity_comment.user_id).first()
    pic['nick_name'] = ''
    pic['picture_path'] = ''
    if user:
        pic['nick_name'] = user.nick_name
        user_info = UserInfo.query.filter(UserInfo.user_id == user.id).first()
        if user_info:
            if user_info.rel_path and user_info.pic_name:
                pic['picture_path'] = user_info.rel_path + '/' + user_info.pic_name


def change_latitude_longitude(pub_pic, pub):
    """
        得到酒吧经度纬度
    """
    if pub:
        pub_pic['latitude'] = str(pub.latitude)
        pub_pic['longitude'] = str(pub.longitude)


class PubGetType(restful.Resource):
    """
    泡吧主页
    """
    @staticmethod
    def get():
        """
        读取所有酒吧
        parser = reqparse.RequestParser()
        parser.add_argument('')
        广告，后期再加上。
        """
        resp_suc = {}
        resp_suc['list'] = []
        # 酒吧所有类型
        pub_types = PubType.query.filter()
        for pub_type in pub_types:
            pub_type_pic = to_flatten(pub_type, pub_type)
            resp_suc['list'].append(pub_type_pic)
        resp_suc['advertising_picture'] = '/static/pub_type_picture/advertising.png'
        resp_suc['status'] = 0
        return resp_suc


class PubListDetail(restful.Resource):
    """
    酒吧分类详细列表
    """
    @staticmethod
    def get():
        """
        需要分类的id
        参数:
            type_id:酒吧类型type_id
            page: 酒吧分页
            city_id: 城市id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('type_id', type=str, required=True, help=u'酒吧类型type_id必须。')
        parser.add_argument('page', type=str, required=True, help=u'分页page必须。')
        parser.add_argument('city_id', type=str, required=False)
        args = parser.parse_args()
        resp_suc = {}
        resp_suc['pub_list'] = []
        resp_suc['picture_list'] = []
        type_id = args['type_id']
        page = args['page']
        if args['type_id']:
            result_count = db.query(PubPicture).\
                join(Pub).\
                join(PubTypeMid).\
                filter(PubTypeMid.pub_type_id == int(args['type_id']), Pub.recommend == 1).\
                group_by(PubPicture.pub_id).count()
            if result_count > 1:
                results = db.query(PubPicture). \
                    join(Pub). \
                    join(PubTypeMid).\
                    filter(PubTypeMid.pub_type_id == int(args['type_id']), Pub.recommend == 1).\
                    group_by(PubPicture.pub_id)
                pub_list_picture(results, resp_suc)
            else:
                result = db.query(PubPicture). \
                    join(Pub). \
                    join(PubTypeMid).\
                    filter(PubTypeMid.pub_type_id == int(args['type_id']), Pub.recommend == 1).\
                    group_by(PubPicture.pub_id).first()
                pub_picture_only(result, resp_suc)
            resp_suc['status'] = 0
            resp_suc['county'] = []
            resp_suc = by_type_id(type_id, resp_suc, page)
            get_county(75, resp_suc)
            return resp_suc
        else:
            resp_suc['message'] = 'error'
            resp_suc['status'] = 1
            return resp_suc


def by_type_id(type_id, resp_suc, page):
    """
       根据type_id来获取酒吧
    """
    pub_type_count = PubTypeMid.query.filter(PubTypeMid.pub_type_id == type_id).count()
    if pub_type_count > 1:
        temp_page = page
        page, per_page, max = page_utils(pub_type_count, page)
        is_max = max_page(temp_page, max, resp_suc)
        if is_max:
            return resp_suc
        pub_types = PubTypeMid.query.filter(PubTypeMid.pub_type_id == type_id).order_by(PubTypeMid.id)[per_page*(int(temp_page)-1):per_page*int(temp_page)]
        for pub_type in pub_types:
            pub = Pub.query.filter(Pub.id == pub_type.pub_id).first()
            pub_only(pub, resp_suc)
        return resp_suc
    else:
        pub_type = PubTypeMid.query.filter(PubTypeMid.pub_type_id == type_id).first()
        if pub_type:
            pub = Pub.query.filter(Pub.id == pub_type.pub_id).first()
            pub_only(pub, resp_suc)
        return resp_suc



class PubDetail(restful.Resource):
    """
    酒吧详细
    """
    @staticmethod
    def get():
        """
        所需参数:
            pub_id:必传，用户所选中的酒吧id
            user_id: 必传，登录用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pub_id', type=str, required=True, help=u'酒吧pub_id必须。')
        parser.add_argument('user_id', type=str, required=False, help=u'登录用户id必须。')
        args = parser.parse_args()
        resp_suc = {}
        resp_suc['picture_list'] = []
        resp_suc['pub_list'] = []
        pub_id = int(args['pub_id'])
        resp_suc['county'] = []

        user_id = args['user_id']
        if pub_id:
            collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == pub_id).first()
            resp_suc['is_collect'] = '收藏'
            if collect:
                resp_suc['is_collect'] = '已收藏'
            pub = Pub.query.filter(Pub.id == pub_id).first()
            pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub_id).first()
            resp_suc['county'] = get_address(pub.province_id, pub.city_id, pub.county_id)
            pub_pic = to_pub_longitude_latitude(pub, pub_picture)
            to_pub_type(pub, pub_pic)
            resp_suc['pub_list'].append(pub_pic)
            view_check = View.query.filter(View.user_id == user_id, View.pub_id == pub_id).first()
            if view_check:
                view_check.view_number = view_check.view_number + 1
                db.commit()
            else:
                user = User.query.filter(User.id == user_id).first()
                if user:
                    view = View(user_id, pub_id, 1)
                    db.add(view)
                    db.commit()
            result_count = db.query(UserInfo).\
                join(User).\
                join(View).\
                filter(View.pub_id == pub_id).order_by(View.time.desc()).count()
            if result_count > 1:
                results = db.query(UserInfo). \
                    join(User). \
                    join(View). \
                    filter(View.pub_id == pub_id).order_by(View.time.desc()).all()
                user_list_picture(results, resp_suc)
            else:
                result = db.query(UserInfo). \
                    join(User). \
                    join(View). \
                    filter(View.pub_id == pub_id).order_by(View.time.desc()).first()
                user_picture_only(result, resp_suc)

            resp_suc['status'] = 0
            resp_suc['message'] = 'success'
            return resp_suc
        else:
            resp_suc['status'] = 1
            resp_suc['message'] = 'error'
            return resp_suc


class PubPictureDetail(restful.Resource):
    """
    酒吧图片列表
    """
    @staticmethod
    def get():
        """
        所需参数:
            pub_id:必传，所点击图片的当前酒吧id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pub_id', type=str, required=True, help=u'酒吧pub_id必须。')

        args = parser.parse_args()
        resp_suc = {}
        pub_id = args['pub_id']
        resp_suc['picture_list'] = []
        # result_count = db.query(UserInfo). \
        #     join(User). \
        #     join(View). \
        #     filter(View.pub_id == pub_id).order_by(View.time.desc()).count()
        # if result_count > 1:
        #     results = db.query(UserInfo). \
        #         join(User). \
        #         join(View). \
        #         filter(View.pub_id == pub_id).order_by(View.time.desc())
        #     user_list_picture(results, resp_suc)
        # else:
        #     result = db.query(UserInfo). \
        #         join(User). \
        #         join(View). \
        #         filter(View.pub_id == pub_id).order_by(View.time.desc()).first()
        #     user_picture_only(result, resp_suc)
        if args['pub_id']:
            pub_id = int(args['pub_id'])
            pub_picture_count = PubPicture.query.filter(PubPicture.pub_id == pub_id).count()
            if pub_picture_count > 1:
                pub_pictures = PubPicture.query.filter(PubPicture.pub_id == pub_id)
                pub_list_picture(pub_pictures, resp_suc)
            else:
                pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub_id).first()
                pub_picture_only(pub_picture, resp_suc)
            resp_suc['message'] = 'success'
            resp_suc['status'] = 0
        else:
            resp_suc['message'] = 'error'
            resp_suc['status'] = 1

        return resp_suc


class PubSearch(restful.Resource):
    """
    搜索酒吧
    """
    @staticmethod
    def get():
        """
        所需参数:
            content:搜索酒吧内容
        """
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True, help=u'content必须，搜索酒吧')
        parser.add_argument('type_id', type=str, required=False)
        parser.add_argument('page', type=str, required=True, help=u'分页page必须.')

        args = parser.parse_args()
        resp_suc = {}
        resp_suc['pub_list'] = []
        resp_fail = fail_dic().dic
        pub_pic = None
        page = args['page']
        if args['content']:
            content = str(args['content'])
            s = "%" + content + "%"
            if args['type_id']:
                pub_count = db.query(Pub).\
                    join(PubTypeMid).\
                    filter(Pub.name.like(s), PubTypeMid.pub_type_id == int(args['type_id'])).count()
                temp_page = page
                page, per_page, max = page_utils(pub_count, page)
                is_max = max_page(temp_page, max, resp_suc)
                if is_max:
                    return resp_suc
                if pub_count == 0:
                    return resp_fail()
                if pub_count > 1:
                    pubs = db.query(Pub). \
                        join(PubTypeMid). \
                        filter(Pub.name.like(s), PubTypeMid.pub_type_id == int(args['type_id']))[per_page*(int(temp_page)-1):per_page*int(temp_page)]
                    pub_list(pubs, resp_suc)
                else:
                    pub = db.query(Pub). \
                        join(PubTypeMid). \
                        filter(Pub.name.like(s), PubTypeMid.pub_type_id == int(args['type_id'])).first()
                    pub_only(pub, resp_suc)
            else:
                pub_count = Pub.query.filter(Pub.name.like(s)).count()
                temp_page = page
                page, per_page, max = page_utils(pub_count, page)
                is_max = max_page(temp_page, max, resp_suc)
                if is_max:
                    return resp_suc
                if pub_count == 0:
                    return resp_fail
                if pub_count > 1:
                    pubs = Pub.query.filter(Pub.name.like(s))[per_page*(int(temp_page)- 1):per_page*int(temp_page)]
                    pub_list(pubs, resp_suc)
                else:
                    pub = Pub.query.filter(Pub.name.like(s)).first()
                    pub_only(pub, resp_suc)

            resp_suc['message'] = "success"
            resp_suc['status'] = 0
            return resp_suc
        else:
            resp_suc['message'] = "error"
            resp_suc['status'] = 1
            return resp_suc


class PubSearchView(restful.Resource):
    """
    搜索界面所需要的数据接口
    """
    @staticmethod
    def get():
        """
        所需参数：
            无
        """
        pub_types = PubType.query.filter()
        resp_suc = {}
        resp_suc['pub_type_list'] = []
        resp_suc['pub_list'] = []
        if pub_types:
            for pub_type in pub_types:
                pub_type_pic = flatten(pub_type)
                resp_suc['pub_type_list'].append(pub_type_pic)
        else:
            resp_suc['status'] = 1
            resp_suc['message'] = 'error'
        pub_count = Pub.query.filter(Pub.recommend == 1).count()
        if pub_count > 1:
            pubs = Pub.query.filter(Pub.recommend == 1)
            pub_list(pubs, resp_suc)
        
        else:
            pub = Pub.query.filter(Pub.recommend == 1).first()
            pub_only(pub, resp_suc)

        resp_suc['status'] = 0
        resp_suc['message'] = 'success'
        return resp_suc


class ActivityInfo(restful.Resource):
    """
        活动详情
    """
    @staticmethod
    def get():
        """
            参数
            activity_id: 活动id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('activity_id', type=str, required=True, help=u'activity_id必须.')

        args = parser.parse_args()

        activity_id = args['activity_id']

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['activity_list'] = []

        activity = Activity.query.filter(Activity.id == activity_id).first()
        if activity:
            activity_pic = pub_activity(activity)
            activity_comment_count = ActivityComment.query.filter(ActivityComment.activity_id == activity.id).count()
            activity_pic['comment_count'] = activity_comment_count
            resp_suc['activity_list'].append(activity_pic)
            return resp_suc
        else:
            return resp_fail


class CommentActivity(restful.Resource):
    """
        活动评论
    """
    @staticmethod
    def get():
        """
            参数：
                activity_id: 活动id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('activity_id', type=str, required=True, help=u'activity_id必须。')

        args = parser.parse_args()

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['comment_list'] = []

        activity_id = args['activity_id']
        activity = Activity.query.filter(Activity.id == activity_id).first()
        if activity:
            activity_comment_count = ActivityComment.query.filter(ActivityComment.activity_id == activity.id).count()
            resp_suc['comment_count'] = activity_comment_count
            comment_user(activity_comment_count, activity, resp_suc)
            return resp_suc
        else:
            return resp_fail


class ActivityList(restful.Resource):
    """
        活动列表
    """
    @staticmethod
    def get():
        """
            参数:
                pub_id: 酒吧id么
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pub_id', type=str, required=False)
        parser.add_argument('page', type=str, required=True, help=u'page必须，当前页码。')

        args = parser.parse_args()

        pub_id = args['pub_id']
        page = args['page']

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['hot_list'] = []
        resp_suc['activity_list'] = []
        if pub_id:
            resp_suc = get_activity_host_list_id(pub_id, resp_suc, page)
            resp_suc = get_activity_list_id(pub_id, resp_suc, page)
        else:
            resp_suc = get_activity_host_list(resp_suc, page)
            resp_suc = get_activity_list(resp_suc, page)
        return resp_suc


def get_activity_host_list_id(pub_id, resp_suc, page):
    """
        获取热门推荐活动
    """
    activity_host_count = Activity.query.filter(Activity.hot == 0, Activity.pub_id == pub_id).count()
    temp_page = page
    page, per_page, max = page_utils(activity_host_count, page)
    is_max = max_page(temp_page, max, resp_suc)
    if is_max:
        return resp_suc
    if activity_host_count > 1:
        activity_host = Activity.query.filter(Activity.hot == 0, Activity.pub_id == pub_id)[per_page*(int(temp_page)-1):per_page*int(temp_page)]
        for host in activity_host:
            host_pic = pub_activity(host)
            resp_suc['hot_list'].append(host_pic)
        return resp_suc
    else:
        activity_host = Activity.query.filter(Activity.hot == 0, Activity.pub_id == pub_id).first()
        host_pic = None
        if activity_host:
            host_pic = pub_activity(activity_host)
        resp_suc['hot_list'].append(host_pic)
        return resp_suc


def get_activity_list_id(pub_id, resp_suc, page):
    """
        获取活动
    """
    activity_host_count = Activity.query.filter(Activity.pub_id == pub_id).count()
    temp_page = page
    page, per_page, max = page_utils(activity_host_count, page)
    is_max = max_page(temp_page, max, resp_suc)
    if is_max:
        return resp_suc
    if activity_host_count > 1:
        activity_host = Activity.query.filter(Activity.pub_id == pub_id)[per_page*(int(temp_page)-1):per_page*int(temp_page)]
        for host in activity_host:
            activity_pic = pub_activity(host)
            resp_suc['activity_list'].append(activity_pic)
        return resp_suc
    else:
        activity_host = Activity.query.filter(Activity.pub_id == pub_id).first()
        activity_pic = None
        if activity_host:
            activity_pic = pub_activity(activity_host)
        resp_suc['activity_list'].append(activity_pic)
        return resp_suc


def get_activity_host_list(resp_suc, page):
    """
        获取热门推荐活动
    """
    activity_host_count = Activity.query.filter(Activity.hot == 0).count()
    temp_page = page
    page, per_page, max = page_utils(activity_host_count, page)
    is_max = max_page(temp_page, max , resp_suc)
    if is_max:
        return resp_suc
    if activity_host_count > 1:
        activity_host = Activity.query.filter(Activity.hot == 0)[per_page*(int(temp_page)-1):per_page*int(temp_page)]
        for host in activity_host:
            host_pic = pub_activity(host)
            resp_suc['hot_list'].append(host_pic)
        return resp_suc
    else:
        activity_host = Activity.query.filter(Activity.hot == 0).first()
        host_pic = None
        if activity_host:
            host_pic = pub_activity(activity_host)
        resp_suc['hot_list'].append(host_pic)
        return resp_suc


def get_activity_list(resp_suc, page):
    """
        获取活动
    """
    activity_host_count = Activity.query.filter().count()
    temp_page = page
    page, per_page, max = page_utils(activity_host_count, page)
    is_max = max_page(temp_page, max, resp_suc)
    if is_max:
        return resp_suc
    if activity_host_count > 1:
        activity_host = Activity.query.filter()[per_page*(int(temp_page)-1):per_page*int(temp_page)]
        for hot in activity_host:
            hot_pic = pub_activity(hot)
            resp_suc['activity_list'].append(hot_pic)
        return resp_suc
    else:
        activity_host = Activity.query.filter().first()
        activity_pic = None
        if activity_host:
            activity_pic = pub_activity(activity_host)
        resp_suc['activity_list'].append(activity_pic)
        return resp_suc


EARTH_RADIUS=6371           # 地球平均半径，6371km
from math import sin, asin, cos, radians, fabs, sqrt, degrees


class NearPub(restful.Resource):
    """
    附近酒吧查询
    """
    @staticmethod
    def get():
        """
        参数
           longitude: 经度
           latitude: 维度
        """
        parser = reqparse.RequestParser()
        parser.add_argument('longitude', type=str, required=True, help=u'longitude必须')
        parser.add_argument('latitude', type=str, required=True, help=u'latitude必须')
        parser.add_argument('page', type=str, required=True, help=u'page当前页必须')

        args = parser.parse_args()

        longitude = float(args['longitude'])
        latitude = float(args['latitude'])
        page = int(args['page'])

        resp_suc = success_dic().dic
        resp_suc['pub_list'] = []
        scope = 5000
        pubs = Pub.query.filter().all()
        longitude_left = longitude + 0.00001 * scope
        longitude_right = longitude - 0.00001 * scope
        latitude_top = latitude + 0.00001 * 1.1 * scope
        latitude_bottom = latitude - 0.00001 * 1.1 * scope
        distance = get_distance_hav(latitude_top, longitude_left, latitude_bottom, longitude_right)

        east_west_longitude = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(latitude))
        east_west_longitude = degrees(east_west_longitude)        # 弧度转换成角度

        south_north_latitude = distance / EARTH_RADIUS
        south_north_latitude = degrees(south_north_latitude)     # 弧度转换成角度
        array = {'left_top': (latitude + south_north_latitude, longitude - east_west_longitude),
        'right_top': (latitude + south_north_latitude, longitude + east_west_longitude),
        'left_bottom': (latitude - south_north_latitude, longitude - east_west_longitude),
        'right_bottom': (latitude - south_north_latitude, longitude + east_west_longitude)}
        left_top = array['left_top']
        right_top = array['right_top']
        left_bottom = array['left_bottom']
        right_bottom = array['right_bottom']
        pub_count = Pub.query.filter(Pub.latitude > right_bottom[0], Pub.latitude < left_top[0],
                                Pub.longitude > left_bottom[1], Pub.longitude < right_top[1]).count()
        temp_page = page
        page, per_page, max = page_utils(pub_count, page)
        is_max = max_page(temp_page, max, resp_suc)
        if is_max:
            return resp_suc
        if pub_count > 1:
            pubs = Pub.query.filter(Pub.latitude > right_bottom[0], Pub.latitude < left_top[0],
                                Pub.longitude > left_bottom[1], Pub.longitude < right_top[1])[per_page*(int(temp_page)-1):per_page*int(temp_page)]
            for pub in pubs:
                pub_only(pub, resp_suc)
        else:
            pub = Pub.query.filter(Pub.latitude > right_bottom[0], Pub.latitude < left_top[0],
                                Pub.longitude > left_bottom[1], Pub.longitude < right_top[1]).first()
            pub_only(pub, resp_suc)

        return resp_suc


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




class ScreeningPub(restful.Resource):
    """
       根据地区来筛选酒吧
    """
    @staticmethod
    def get():
        """
            参数
               county_ic: 区域id
               page: 分页
               type_id: 所在酒吧类型
        """
        parser = reqparse.RequestParser()
        parser.add_argument('county_id', type=str, required=True, help=u'county_id必须')
        parser.add_argument('page', type=str, required=True, help=u'page必须')
        parser.add_argument('type_id', type=str, required=True, help=u'type_id必须')

        args = parser.parse_args()

        county_id = args['county_id']
        page = args['page']
        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['pub_list'] = []
        type_id = args['type_id']
        if county_id == '0':
            resp_suc = by_type_id(type_id, resp_suc, page)
            return resp_suc
        else:
            resp_suc = get_pub(type_id, resp_suc, page, county_id)
            return resp_suc


def get_pub(type_id, resp_suc, page, county_id):
    """
       获取酒吧
    """
    pub_type_count = PubTypeMid.query.filter(PubTypeMid.pub_type_id == type_id).count()
    if pub_type_count > 1:
        temp_page = page
        page, per_page,max = page_utils(pub_type_count, page)
        is_max = max_page(temp_page, max, resp_suc)
        if is_max:
            return resp_suc
        pub_types = PubTypeMid.query.filter(PubTypeMid.pub_type_id == type_id)[per_page*(int(temp_page)-1):per_page*int(temp_page)]
        for pub_type in pub_types:
            pub = Pub.query.filter(Pub.id == pub_type.pub_id, Pub.county_id == county_id).first()
            pub_only(pub, resp_suc)
        return resp_suc
    else:
        pub_type = PubTypeMid.query.filter(PubTypeMid.pub_type_id == type_id, Pub.county_id == county_id).first()
        if pub_type:
            pub = Pub.query.filter(Pub.id == pub_type.pub_id).first()
            pub_only(pub, resp_suc)
        return resp_suc