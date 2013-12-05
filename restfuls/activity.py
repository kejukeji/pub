# coding: UTF-8

from flask.ext import restful
from flask.ext.restful import reqparse
from utils.others import success_dic, fail_dic, flatten
from models.activity import Activity, ActivityPicture
from models.pub import Pub


def get_activity_by_id(id):
    """
    通过id得到activity
    """
    activity = Activity.query.filter(Activity.id == id).first()
    if activity:
        by_activity_id_get_address(activity)
        activity = flatten(activity)
        return activity
    return None


def by_activity_id_get_address(activity):
    """
    通过活动中酒吧id得到地址
    """
    pub = Pub.query.filter(Pub.id == activity.pub_id).first()
    if pub.street:
        activity.address = pub.street
    else:
        activity.address = '未填写'


def get_activity_picture(activity):
    """
    获取活动图片
    """
    result = is_list(activity)
    if result != -1:
        format_picture_path(result)
        if type(result) is list:
            temp_list = []
            for r in result:
                r_pic = flatten(r)
                temp_list.append(r_pic)
            return temp_list
        else:
            result_pic = flatten(result)
            return result_pic
    else:
        return None


def format_picture_path(obj):
    if obj.rel_path and obj.pic_name:
        obj.pic_path = obj.rel_path + "/" + obj.pic_name


def is_list(activity):
    """
    获取图片是否有多张
    """
    activity_picture_count = ActivityPicture.query.filter(ActivityPicture.activity_id == activity).count()
    if activity_picture_count > 1:
        activity_picture = ActivityPicture.query.filter(ActivityPicture.activity_id == activity).all()
        return activity_picture
    elif activity_picture_count == 1:
        activity_picture = ActivityPicture.query.filter(ActivityPicture.activity_id == activity).first()
        return activity_picture
    else:
        return -1


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

        args = parser.parse_args()

        activity_id = args['activity_id']

        success = success_dic().dic
        fail = fail_dic().dic

        activity = get_activity_by_id(activity_id)

        if activity:
            result = get_activity_picture(activity_id)
            success['activity_picture'] = result
            success['activity'] = activity
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