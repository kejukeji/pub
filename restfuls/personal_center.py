# coding: UTF-8

from flask.ext import restful
from flask.ext.restful import reqparse
from utils.others import *
from models.feature import *
from models.user import UserInfo as ModelUserInfo, User
from models.level import *
from restfuls.user_function import traverse_messages_sender, traverse_message_sender
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
    user_private_letter = db.query(Message).\
        filter(Message.receiver_id == user_id).\
        group_by(Message.sender_id).count()
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
    user_info.private_letter = get_user_private_letter(user_id)
    return user_info


def get_gift(user_id):
    """
    获得礼物根据user_id
    """
    gift_count = UserGift.query.filter(UserGift.receiver_id == user_id).count()
    return gift_count


def add_picture_user(picture, obj):
    """
    有图片的对象，格式化图片路劲
    """
    if picture.rel_path and picture.pic_name:
        obj.pic_path = picture.rel_path + "/" + picture.pic_name
    else:
        obj.pic_path = ''


def add_picture(obj):
    """
    有图片的对象，格式化图片路劲
    """
    if obj:
        if obj.rel_path and obj.pic_name:
            obj.pic_path = obj.rel_path + "/" + obj.pic_name
        else:
            obj.pic_path = ''


def get_gift_all(success, page):
    """
    获得全部礼物
    """
    success['gift'] = []
    gift_count = Gift.query.filter(Gift.status == 1).count()
    if gift_count > 1:
        gift_all = Gift.query.filter(Gift.status == 1).all()
        if gift_all:
            for gift in gift_all:
                add_picture(gift)
                gift_pic = flatten(gift)
                success['gift'].append(gift_pic)
            return True
        else:
            return False
    else:
        gift_first = Gift.query.filter(Gift.status == 1).first()
        if gift_first:
            add_picture(gift_first)
            gift_pic = flatten(gift_first)
            success['gift'].append(gift_pic)
            return True
        else:
            return False


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
        else:
            obj.nick_name = ''
        add_picture_user(user_info, obj)
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


class InvitationReceiver(restful.Resource):
    """
    邀约
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


class GreetingReceiver(restful.Resource):
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
        if gift:
            if gift and gift.rel_path and gift.pic_name:
                user_gift.gift_pic_path = gift.rel_path + "/" + gift.pic_name
            else:
                user_gift.gift_pic_path = ''
            if gift.name:
                user_gift.gift_name = gift.name
            else:
                user_gift.gift_name = ''


def get_gift_by_id(user_id, page, success, gift_type):
    """
    获取礼物通过user_id
    """
    success['gift'] = []
    user_gift_count = UserGift.query.filter(UserGift.receiver_id == user_id).count()
    temp_page = int(page)
    is_all = True
    if gift_type == 'personal':
        page, per_page, max = page_utils(user_gift_count, page)
        is_all = False
    else:
        page, per_page, max = page_utils(user_gift_count, page, per_page=20)
        is_all = True
    if user_gift_count > 1:
        if is_all:
            user_gift = UserGift.query.filter(UserGift.receiver_id == user_id).all()
        else:
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


class GiftReceiver(restful.Resource):
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
        parser.add_argument('gift_type', type=str, required=True, help=u'gift_type 必须,如果是个人中心，值为personal，好友中心礼物为friend')

        args = parser.parse_args()

        success = success_dic().dic

        user_id = args['user_id']
        page = args['page']
        gift_type = args.get('gift_type', 'personal')

        is_true = get_gift_by_id(user_id, page, success, gift_type)
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
        user_info = ModelUserInfo.query.filter(ModelUserInfo.user_id == receiver_id).first()
        user_info.add_credit('invite') # 增加接受者积分
        db.commit()
        sender_user = ModelUserInfo.query.filter(ModelUserInfo.user_id == sender_id).first()
        sender_user.add_reputation('invite') # 增加发送者经验值
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
            success['message'] = '发送成功'
            return success
        else:
            success['message'] = '发送失败'
            return success


def sender_gift(sender_id, receiver_id, gift_id):
    """
    发送礼物
    """
    gift = UserGift(sender_id=sender_id, receiver_id=receiver_id, gift_id=gift_id)
    try:
        db.add(gift)
        db.commit()
        user_info = ModelUserInfo.query.filter(ModelUserInfo.user_id == receiver_id).first()
        user_info.add_credit('gift') # 增加接受者积分
        db.commit()
        sender_user = ModelUserInfo.query.filter(ModelUserInfo.user_id == sender_id).first()
        sender_user.add_reputation('gift') # 增加发送者经验值
        db.commit()
    except:
        return False
    return True


class SenderGift(restful.Resource):
    """
    发送礼物
    """
    @staticmethod
    def get():
        """
        sender_id: 发送者id
        receiver_id: 接受者id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=str, required=True, help=u'sender_id 必须')
        parser.add_argument('receiver_id', type=str, required=True, help=u'receiver_id 必须')
        parser.add_argument('gift_id', type=str, required=True, help=u'gift_id 必须')

        args = parser.parse_args()

        success = success_dic().dic

        sender_id = args['sender_id']
        receiver_id = args['receiver_id']
        gift_id = args['gift_id']

        is_true = sender_gift(sender_id, receiver_id, gift_id)
        if is_true:
            success['message'] = '发送成功'
            return success
        else:
            success['message'] = '发送失败'
            return success


class SenderGiftView(restful.Resource):
    """
    发送礼物的界面
    """
    @staticmethod
    def get():
        success = success_dic().dic

        is_true = get_gift_all(success, 1)
        if is_true:
            return success
        else:
            success['message'] = '没有数据'
            return success


def sender_greeting(sender_id, receiver_id):
    """
    发送传情
    """
    greeting = Greeting(sender_id=sender_id, receiver_id=receiver_id)
    try:
        db.add(greeting)
        db.commit()
        result = db.query(Greeting).\
            filter(Greeting.sender_id == sender_id).\
            group_by(Greeting.sender_id).count()
        if result == 0:
            user_info = ModelUserInfo.query.filter(ModelUserInfo.user_id == receiver_id).first()
            user_info.add_credit('greet') # 增加接受者积分
            db.commit()
            sender_user = ModelUserInfo.query.filter(ModelUserInfo.user_id == sender_id).first()
            sender_user.add_reputation('greet') # 增加发送者经验值
            db.commit()
    except:
        return False
    return True


class SenderGreeting(restful.Resource):
    """
    发送传情
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

        is_true = sender_greeting(sender_id, receiver_id)
        if is_true:
            success['message'] = '发送成功'
            return success
        else:
            success['message'] = '发送失败'
            return success


def get_private_letter_list(user_id, page, success):
    """
    获取个人中心的私心列表。看清楚了哦。 是个人中心的。 而不是消息的。。 这坑爹的设计我他妈的无力吐槽。
    """
    success['sender_list'] = []
    message_count = db.query(Message).\
        filter(Message.receiver_id == user_id).order_by(Message.time.desc()).\
        group_by(Message.sender_id).count()
    temp_page = int(page)
    page,per_page, max = page_utils(message_count, page)
    if message_count > 1:
        direct_messages = db.query(Message).\
            filter(Message.receiver_id == user_id).order_by(Message.time.desc()).\
            group_by(Message.sender_id)[per_page * (temp_page -1):per_page * temp_page]
        traverse_messages_sender(direct_messages, success)
        return True
    elif message_count == 1:
        direct_message = db.query(Message). \
            filter(Message.receiver_id == user_id).order_by(Message.time.desc()). \
            group_by(Message.sender_id).first()
        traverse_message_sender(direct_message, success)
        return True
    else:
        return False


class PersonalPrivateLetter(restful.Resource):
    """
    个人中心私信列表
    """
    @staticmethod
    def get():
        """
        user_id: 用户id
        page: 分页
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')
        parser.add_argument('page', type=str, required=True, help=u'page 必须')

        args = parser.parse_args()

        success = success_dic().dic

        user_id = args['user_id']
        page = args['page']

        is_true = get_private_letter_list(user_id, page, success)
        if is_true:
            return success
        else:
            success['message'] = '没有数据'
            return success


def get_reputation_difference(reputation):
    '''获得当前经验值距离下一个等级还需经验值'''
    level = Level.query.filter(Level.min <= reputation,Level.max >= reputation).order_by(desc(Level.level)).first()
    next_level = Level.query.filter(Level.level == level.level + 1).first() # 得到下一等级
    reputation_difference = next_level.min - reputation # 最小经验值减去当前经验值等于相差经验值
    return reputation_difference


def get_user_credit_reputation(user_id, success):
    '''获取用户积分以及经验值'''
    user_result = ModelUserInfo.query.filter(ModelUserInfo.user_id == user_id).first()
    success['credit'] = 0
    success['reputation'] = 0
    success['reputation_difference'] = 0 # 距离下一等级还需经验值
    if user_result:
        credit = user_result.credit # 积分
        reputation = user_result.reputation # 经验值
        # 保存到返回客户端字典当中
        success['credit'] = credit
        success['reputation'] = reputation
        success['reputation_difference'] = get_reputation_difference(reputation)
        return True
    else:
        return False


class CreditRule(restful.Resource):
    """
    积分规则
       当前经验值，离下一等级还需经验值
       当前拥有积分
    """
    @staticmethod
    def get():
        """
        user_id: 登陆用户id
        """
        parser = reqparse.RequestParser()
        # 定义客户端传入参数
        parser.add_argument('user_id', type=str, required=True, help=u'user_id 必须')

        args = parser.parse_args() # 得到参数对象

        success = success_dic().dic # 返回客户端字典

        user_id = args['user_id'] # 得到客户端传入参数
        # 获取积分，经验，相差经验
        is_true = get_user_credit_reputation(user_id, success)
        if is_true:
            return success
        else:
            success['message'] = '没有数据'
            return success