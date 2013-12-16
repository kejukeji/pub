# coding: UTF-8

from flask.ext import restful
from flask.ext.restful import reqparse
from utils.others import *
from models.feature import *
from models.user import UserInfo as ModelUserInfo, User
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


def get_user_nickname_picture(user_id):
    """
    获取用户昵称，头像
    """
    user = User.query.filter(User.id == user_id).first()  # 获得发送用户昵称
    user_info = ModelUserInfo.query.filter(ModelUserInfo.user_id == user.id).first() # 获得发送用户头像
    return user, user_info


def format_common(invitation):
    if invitation:
        user, user_info = get_user_nickname_picture(invitation.sender_id)
        if user:
            invitation.nick_name = user.nick_name
        if user_info and user_info.rel_path and user_info.pic_name:
            invitation.pic_path = user_info.rel_path + "/" + user_info.pic_name
        return True
    else:
        return False


def get_invitation_by_id(user_id, page, success):
    """
    根据user_id获取...
    """
    invitation_count = Invitation.query.filter(Invitation.receiver_id == user_id).count()
    temp_page = int(page)
    page, per_page, max = page_utils(invitation_count, page)
    if invitation_count > 1:
        invitation = Invitation.query.filter(Invitation.receiver_id == user_id)[per_page * (temp_page - 1):per_page * temp_page]
        is_true = True
        for i in invitation:
            is_true = format_common(i)
            invitation_pic = flatten(i)
            success['invitation'].append(invitation_pic)
        return is_true
    else:
        invitation = Invitation.query.filter(Invitation.receiver_id == user_id).first()
        is_true = format_common(invitation)
        if is_true:
            invitation_pic = flatten(invitation)
            success['invitation'].append(invitation_pic)
            return True
        else:
            return False


class InvitationView(restful.Resource):
    """
    邀约界面
    """
    @staticmethod
    def get():
        """
        user_id: 用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')
        parser.add_argument('page', type=str, required=True, help=u'page 必须')

        args = parser.parse_args()

        success = success_dic().dic

        user_id = args['user_id']
        page = args['page']

        success['invitation'] = []

        is_true = get_invitation_by_id(user_id, page, success)
        if is_true:
            return success
        else:
            success['message'] = '没有数据'
            return success



def get_greeting_by_id(user_id, page, success):
    """
    获取传情根据user_id
    """
    greeting_count = Greeting.query.filter(Greeting.receiver_id == user_id).count()
    temp_page = int(page)
    page, per_page, max = page_utils(greeting_count, page)
    if greeting_count > 1:
        greeting = Greeting.query.filter(Greeting.receiver_id == user_id)[per_page * (temp_page -1):per_page * temp_page]
        is_true = True
        for g in greeting:
            is_true = format_common(g)
            g_pic = flatten(g)
            success['greeting'].append(g_pic)
        return is_true
    else:
        greeting = Greeting.query.filter(Greeting.receiver_id == user_id).first()
        is_true = format_common(greeting)
        if is_true:
            invitation_pic = flatten(greeting)
            success['greeting'].append(invitation_pic)
            return True
        else:
            return False


class GreetingView(restful.Resource):
    """
    传情
    """
    @staticmethod
    def get():
        """
        user_id : 用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')
        parser.add_argument('page', type=str, required=True, help=u'page 必须')

        args = parser.parse_args()

        success = success_dic().dic

        user_id = args['user_id']
        page = args['page']

        success['greeting'] = []

        is_true = get_greeting_by_id(user_id, page, success)
        if is_true:
            return success
        else:
            success['message'] = '没有数据'
            return success