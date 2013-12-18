# coding: UTF-8

from flask.ext import restful
from flask.ext.restful import reqparse
from utils.others import *
from models.feature import *
from models.user import UserInfo as ModelUserInfo, User
from models.level import *
from models import db


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


def format_common(obj):
    if obj:
        user, user_info = get_user_nickname_picture(obj.sender_id)
        if user:
            obj.nick_name = user.nick_name
        if user_info and user_info.rel_path and user_info.pic_name:
            obj.pic_path = user_info.rel_path + "/" + user_info.pic_name
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


def get_gift_image(user_gift):
    """
    获取礼物图片
    """
    if user_gift:
        gift = Gift.query.filter(Gift.id == user_gift.gift_id).first()
        if gift and gift.rel_path and gift.pic_name:
            user_gift.gift_pic_path = gift.rel_path + "/" + gift.pic_name


def get_gift_by_id(user_id, page, success):
    """
    获取礼物通过user_id
    """
    success['gift'] = []
    user_gift_count = UserGift.query.filter(UserGift.receiver_id == user_id).count()
    temp_page = int(page)
    page, per_page, max = page_utils(user_gift_count, page)
    if user_gift_count > 1:
        user_gift = UserGift.query.filter(UserGift.receiver_id == user_id)[per_page * (temp_page - 1):per_page * temp_page]
        is_true = True
        if user_gift:
            for user in user_gift:
                is_true = format_common(user)
                get_gift_image(user)
                user_pic = flatten(user)
                success['gift'].append(user_pic)
        return is_true
    else:
        user_gift = UserGift.query.filter(UserGift.receiver_id == user_id).first()
        is_true = format_common(user_gift)
        get_gift_image(user_gift)
        if is_true:
            invitation_pic = flatten(user_gift)
            success['gift'].append(invitation_pic)
            return True
        else:
            return False


class GiftViewX(restful.Resource):
    """
    礼物列表
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

        is_true = get_gift_by_id(user_id, page, success)
        if is_true:
            return success
        else:
            success['message'] = '没有数据'
            return success


def sender_invitation(sender_id, receiver_id):
    """
    发送一个邀约
    """
    invitation = Invitation(sender_id=sender_id, receiver_id=receiver_id)
    try:
        db.add(invitation)
        db.commit()
    except:
        return False
    return True



class SenderInvite(restful.Resource):
    """
    发送邀约
    """
    @staticmethod
    def get():
        """
        sender_id: 发送者id
        receiver_id: 接收者id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=str, required=True, help=u'sender_id 必须')
        parser.add_argument('receiver_id', type=str, required=True, help=u'receiver_id 必须')

        args = parser.parse_args()

        success = success_dic().dic

        sender_id = args['sender_id']
        receiver_id = args['receiver_id']

        is_true = sender_invitation(sender_id, receiver_id)
        if is_true:
            return success
        else:
            success['message'] = '发送失败'
            return success