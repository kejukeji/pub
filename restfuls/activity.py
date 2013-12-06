# coding: UTF-8

from flask.ext import restful
from flask.ext.restful import reqparse
from utils.others import success_dic, fail_dic, flatten, page_utils
from models.activity import Activity, ActivityPicture
from models.pub import Pub
from models.feature import UserActivity
from models.database import db


def get_activity_by_id(id, user_id):
    """
    通过id得到activity
    """
    activity = Activity.query.filter(Activity.id == id).first()
    if activity:
        get_activity_address_by_id(activity)
        activity_is_collect(activity, user_id)
        activity = flatten(activity)
        return activity
    return None


def get_activity_address_by_id(activity):
    """
    通过活动中酒吧id得到地址
    """
    pub = Pub.query.filter(Pub.id == activity.pub_id).first()
    if pub.street:
        activity.address = pub.street
    else:
        activity.address = '未填写'


def activity_is_collect(activity, user_id):
    """
    查看是否收藏
    """
    user_activity = UserActivity.query.filter(UserActivity.user_id == user_id, UserActivity.activity_id == activity.id).first()
    if user_activity:
        activity.is_collect = True
    else:
        activity.is_collect = False


def get_activity_picture(id):
    """
    获取活动图片
    """
    result = is_list(id)
    if result != -1:

        if type(result) is list:
            temp_list = []
            for r in result:
                format_picture_path(r)
                r_pic = flatten(r)
                temp_list.append(r_pic)
            return temp_list
        else:
            format_picture_path(result)
            result_pic = flatten(result)
            return result_pic
    else:
        return None


def format_picture_path(obj):
    if obj.rel_path and obj.pic_name:
        obj.pic_path = obj.rel_path + "/" + obj.pic_name


def is_list(id):
    """
    获取图片是否有多张
    """
    activity_picture_count = ActivityPicture.query.filter(ActivityPicture.activity_id == id).count()
    if activity_picture_count > 1:
        activity_picture = ActivityPicture.query.filter(ActivityPicture.activity_id == id).all()
        return activity_picture
    elif activity_picture_count == 1:
        activity_picture = ActivityPicture.query.filter(ActivityPicture.activity_id == id).first()
        return activity_picture
    else:
        return -1


def get_activity_by_pub_id(pub_id, user_id):
    """
    通过酒吧id得到所属最新活动
    """
    activity = Activity.query.filter(Activity.pub_id == pub_id).order_by(Activity.start_date.desc()).first()
    if activity:
        activity_is_collect(activity, user_id)
        activity_picture = ActivityPicture.query.filter(ActivityPicture.activity_id == activity.id).first()
        if activity_picture:
            if activity_picture.rel_path and activity_picture.pic_name:
                activity.pic_path = activity_picture.rel_path + "/" + activity_picture.pic_name
        activity = flatten(activity)
    return activity


class ActivityInfo(restful.Resource):
    """
    活动详情
    """
    @staticmethod
    def get():
        """
        activity_id: 活动id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('activity_id', type=str, required=True, help=u'activity_id 必须')
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')

        args = parser.parse_args()

        activity_id = args['activity_id']
        user_id = args['user_id']

        success = success_dic().dic
        fail = fail_dic().dic

        success['activity_picture'] = []

        activity = get_activity_by_id(activity_id, user_id)

        if activity:
            result = get_activity_picture(activity_id)
            if type(result) is list:
                success['activity_picture'] = result
            else:
                success['activity_picture'].append(result)
            success['activity'] = activity
            return success
        else:
            return fail


def collect_or_cancel_activity(user_id, activity_id):
    """
    收藏或者，取消收藏
    """
    user_activity = UserActivity.query.filter(UserActivity.user_id == user_id, UserActivity.activity_id == activity_id).first()
    if user_activity:
        try:
            db.delete(user_activity)
            db.commit()
            return True
        except:
            return False
    else:
        user_activity = UserActivity(user_id=user_id, activity_id=activity_id)
        try:
            db.add(user_activity)
            db.commit()
            return True
        except:
            return False



class CollectActivity(restful.Resource):
    """
    收藏活动
    """
    @staticmethod
    def get():
        """
        activity_id: 活动id
        user_id: 用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('activity_id', type=str, required=True, help=u'activity_id 必须')
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')

        args = parser.parse_args()

        success = success_dic().dic
        fail = fail_dic().dic

        activity_id = args['activity_id']
        user_id = args['user_id']

        result = collect_or_cancel_activity(user_id, activity_id)
        if result:
            return success
        else:
            return fail


def activity_collect_list(user_id, page, success):
    """
    得到用户活动收藏列表
    """
    user_activity_count = UserActivity.query.filter(UserActivity.user_id == user_id).count()
    if user_activity_count > 1:
        temp_page = page
        page, per_page, max = page_utils(user_activity_count, page)
        user_activity = UserActivity.query.filter(UserActivity.user_id == user_id)[page * (temp_page - 1): per_page * temp_page]
        activity_pic = ''
        for u in user_activity:
            activity = Activity.query.filter(Activity.id == u.activity_id).first()
            if activity:
                activity.collect_time = u.time
                list_result = is_list(activity.id)
                if type(list_result) is list:
                    format_picture_path(list_result[0])
                    if list_result[0].pic_path:
                        activity.pic_path = list_result[0].pic_path
                else:
                    format_picture_path(list_result)
                    if list_result.pic_path:
                        activity.pic_path = list_result.pic_path
                belong_pub_name(activity)
                activity_is_collect(activity, user_id)
                activity_pic = flatten(activity)
                success['activity_collect'].append(activity_pic)
    else:
        user_activity = UserActivity.query.filter(UserActivity.user_id == user_id).first()
        if user_activity:
            activity = Activity.query.filter(Activity.id == user_activity.activity_id).first()
            if activity:
                activity.collect_time = user_activity.time
                list_result = is_list(activity.id)
                if type(list_result) is list:
                    format_picture_path(list_result[0])
                    if list_result[0].pic_path:
                        activity.pic_path = list_result[0].pic_path
                else:
                    format_picture_path(list_result)
                    if list_result.pic_path:
                        activity.pic_path = list_result.pic_path
                belong_pub_name(activity)
                activity_is_collect(activity, user_id)
                activity_pic = flatten(activity)
                success['activity_collect'].append(activity_pic)
    return user_activity_count


def belong_pub_name(activity):
    pub = Pub.query.filter(Pub.id == activity.pub_id).first()
    if pub:
        activity.pub_name = pub.name



class ActivityCollectList(restful.Resource):
    """
    活动收藏列表
    """
    @staticmethod
    def get():
        """
        user_id: 登陆id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')
        parser.add_argument('page', type=str, required=True, help=u'page 必须')

        args = parser.parse_args()

        success = success_dic().dic
        fail = fail_dic().dic

        success['activity_collect'] = []

        user_id = args['user_id']
        page = int(args['page'])

        result = activity_collect_list(user_id, page, success)
        if result != 0:
            return success
        else:
            return fail


#class ActivityInfo(restful.Resource):
#    """
#        活动详情
#    """
#    @staticmethod
#    def get():
#        """
#            参数
#            activity_id: 活动id
#        """
#        parser = reqparse.RequestParser()
#        parser.add_argument('activity_id', type=str, required=True, help=u'activity_id必须.')
#
#        args = parser.parse_args()
#
#        activity_id = args['activity_id']
#
#        resp_suc = success_dic().dic
#        resp_fail = fail_dic().dic
#        resp_suc['activity_list'] = []
#
#        activity = Activity.query.filter(Activity.id == activity_id).first()
#        if activity:
#            activity_pic = pub_activity(activity)
#            activity_comment_count = ActivityComment.query.filter(ActivityComment.activity_id == activity.id).count()
#            activity_pic['comment_count'] = activity_comment_count
#            resp_suc['activity_list'].append(activity_pic)
#            return resp_suc
#        else:
#            return resp_fail