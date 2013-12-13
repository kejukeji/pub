# coding: UTF-8

from flask.ext import restful
from flask.ext.restful import reqparse
from utils.others import *
from models.feature import *
from models.user import UserInfo as ModelUserInfo
from models.level import *


def get_user_collect_activity(user_id):
    """
    根据user_id获取用户收藏的活动
    """
    user_collect_count = UserActivity.query.filter(UserActivity.user_id == user_id).count()
    return user_collect_count


def get_user_collect_pub(user_id):
    """
    根据user_id获取用户收藏酒吧
    """
    user_collect_pub = Collect.query.filter(Collect.user_id == user_id).count()
    return user_collect_pub


def get_user_private_letter(user_id):
    """
    根据user_id获取用户私信
    """
    user_private_letter = Message.query.filter(Message.receiver_id == user_id, Message.view == 0).count()
    return user_private_letter


def get_user(user_id):
    """
    根据user_id获取用户积分,等级
    """
    user_info = ModelUserInfo.query.filter(ModelUserInfo.user_id == user_id).first()
    level = Level.query.filter().all()
    if level and type(level) is list:
        for l in level:
            reputation = user_info.reputation
            if reputation >= l.min and reputation <= l.max:
                user_info.level = l.short_name
                user_info.level_description = l.long_name
    user_collect_activity_count = get_user_collect_activity(user_id)
    user_info.collect_activity_count = user_collect_activity_count
    user_collect_pub_count = get_user_collect_pub(user_id)
    user_info.collect_pub_count = user_collect_pub_count
    user_greeting = get_greeting(user_id)
    user_info.greeting_count = user_greeting
    user_private_letter_count = get_user_private_letter(user_id)
    user_info.private_letter_count = user_private_letter_count
    user_invitation = get_invitation(user_id)
    user_info.invitation = user_invitation
    user_info.gift = get_gift(user_id)
    return user_info


def get_gift(user_id):
    """
    获得礼物
    """
    gift_count = UserGift.query.filter(UserGift.receiver_id == user_id).count()
    return gift_count


def get_greeting(user_id):
    """
    获取传情
    """
    greeting_count = Greeting.query.filter(Greeting.receiver_id == user_id).count()
    return greeting_count


def get_invitation(user_id):
    """
    获取邀请
    """
    invitation_count = Invitation.query.filter(Invitation.receiver_id == user_id).count()
    return invitation_count



class PersonCenter(restful.Resource):
    """
    个人中心
    """
    @staticmethod
    def get():
        """
        user_id: 用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')

        args = parser.parse_args()

        user_id = args['user_id']

        success = success_dic().dic
        user = get_user(user_id)

        success['user'] = flatten(user)

        return success
