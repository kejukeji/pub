# coding: utf-8

from flask.ext import restful
from sqlalchemy.orm import Session, sessionmaker
from models import Collect, Pub, User, engine, db, Message, UserInfo, PubPicture, County, SystemMessage, FeedBack, UserSystemMessage
from flask.ext.restful import reqparse
from utils import pickler, time_diff, page_utils, todayfstr
from datetime import datetime
from utils.others import success_dic, fail_dic
from utils.others import time_to_str, flatten, max_page


def differences(obj, time_dif):
    """
    计算时间差
    """
    obj_pic = flatten(obj)
    obj_pic['difference'] = time_dif
    return obj_pic


def change_latitude_longitude(pub_pic, pub):
    """
        得到酒吧经度纬度
    """
    if pub:
        pub_pic['latitude'] = str(pub.latitude)
        pub_pic['longitude'] = str(pub.longitude)


def get_year(time):
    if time:
        dt = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
        today = datetime.today()
        s = int((today - dt).total_seconds())
        return str(s / 3600 / 24 / 365)
    else:
        return ''



def to_messages(times, content, message_id):
    """
    用户发送时间times
    用户发送内容content
    """
    user = User.query.filter(User.id == message_id).first()
    user_info = UserInfo.query.filter(UserInfo.user_id == user.id).first()
    json_pic = flatten(user)
    if user_info:
        sex = user_info.sex
        birthday = None
        if user_info.birthday:
            birthday = user_info.birthday
        age = get_year(birthday)
        json_pic = flatten(user)
        if user_info.rel_path and user_info.pic_name:
            json_pic['pic_path'] = user_info.rel_path + '/' + user_info.pic_name
        if sex == 1:
            json_pic['sex'] = '男'
        else:
            json_pic['sex'] = '女'
        json_pic['age'] = age
    json_pic['send_time'] = times
    json_pic['content'] = content
    return json_pic


def to_messages_no_time(content, message_id):
    """
    用户发送时间times
    用户发送内容content
    """
    user = User.query.filter(User.id == message_id).first()
    if user:
        user_info = UserInfo.query.filter(UserInfo.user_id == user.id).first()
        json_pic = flatten(user)
        if user_info:
            sex = user_info.sex
            birthday = None
            if user_info.birthday:
                birthday = user_info.birthday
            age = get_year(birthday)
            json_pic = flatten(user)
            if user_info.rel_path and user_info.pic_name:
                json_pic['receiver_path'] = user_info.rel_path + '/' + user_info.pic_name
            if sex == 1:
                json_pic['sex'] = '男'
            else:
                json_pic['sex'] = '女'
            json_pic['age'] = age
        json_pic['content'] = content
        return json_pic
    else:
        return {}


def to_messages_sender(content, message_id):
    """
    用户发送时间times
    用户发送内容content
    """
    user = User.query.filter(User.id == message_id).first()
    if user:
        user_info = UserInfo.query.filter(UserInfo.user_id == user.id).first()
        json_pic = flatten(user)
        if user_info:
            sex = user_info.sex
            birthday = None
            if user_info.birthday:
                birthday = user_info.birthday
            age = get_year(birthday)
            json_pic = flatten(user)
            if user_info.rel_path and user_info.pic_name:
                json_pic['receiver_path'] = user_info.rel_path + '/' + user_info.pic_name
            if sex == 1:
                json_pic['sex'] = '男'
            else:
                json_pic['sex'] = '女'
            json_pic['age'] = age
        json_pic['content'] = content
        return json_pic
    else:
        return {}


def traverse_messages(messages, resp_suc):
    """
        遍历多条消息
    """
    if messages:
        for message in messages:
            times = time_diff(message.time)
            content = message.content
            user_pic = to_messages(times, content, message.sender_id)
            user_pic['sender_id'] = message.sender_id
            user_pic['receiver_id'] = message.receiver_id
            time = time_to_str(message.time)
            user_pic['time'] = time
            resp_suc['list'].append(user_pic)


def traverse_messages_sender(messages, resp_suc):
    """
        遍历多条消息
    """
    if messages:
        for message in messages:
            user_pic = to_messages_no_time(message.content, message.sender_id)
            user_pic['sender_id'] = message.sender_id
            user_pic['receiver_id'] = message.receiver_id
            time = time_to_str(message.time)
            user_pic['time'] = time
            resp_suc['sender_list'].append(user_pic)


def traverse_messages_receiver(messages, resp_suc):
    """
        遍历接收多条消息
    """
    #if receiver_messages:
    #    for message in receiver_messages:
    #        user_pic = to_messages_no_time(message.content, message.sender_id)
    #        user_pic['sender_id'] = message.sender_id
    #        user_pic['receiver_id'] = message.receiver_id
    #        time = time_to_str(message.time)
    #        user_pic['time'] = time
    #        resp_suc['list'].append(user_pic)
    if messages:
        for message in messages:
            message.view = 1
            db.commit()
            times = time_diff(message.time)
            user_pic = to_messages(times, message.content, message.sender_id)
            user_pic['sender_id'] = message.sender_id
            user_pic['receiver_id'] = message.receiver_id
            time = time_to_str(message.time)
            user_pic['time'] = time
            resp_suc['list'].append(user_pic)


def traverse_message(message, resp_suc):
    """
        遍历一条消息
    """
    if message:
        times = time_diff(message.time)
        content = message.content
        user_pic = to_messages(times, content, message.sender_id)
        user_pic['sender_id'] = message.sender_id
        user_pic['receiver_id'] = message.receiver_id
        time = time_to_str(message.time)
        user_pic['time'] = time
        resp_suc['list'].append(user_pic)


def traverse_message_sender(message, resp_suc):
    """
        遍历发送一条消息
    """
    if message:
        user_pic = to_messages_no_time(message.content, message.sender_id)
        user_pic['sender_id'] = message.sender_id
        user_pic['receiver_id'] = message.receiver_id
        time = time_to_str(message.time)
        user_pic['sender_time'] = time
        resp_suc['sender_list'].append(user_pic)


def traverse_message_receiver(sender_message, resp_suc):
    """
        遍历接收一条消息
    """
    #if message:
    #    times = time_diff(message.time)
    #    content = message.content
    #    user_pic = to_messages(times, content, message.sender_id)
    #    user_pic['sender_id'] = message.sender_id
    #    user_pic['receiver_id'] = message.receiver_id
    #    time = time_to_str(message.time)
    #    user_pic['time'] = time
    #    resp_suc['list'].append(user_pic)
    if sender_message:
        sender_message.view = 1
        db.commit()
        times = time_diff(sender_message.time)
        content = sender_message.content
        user_pic = to_messages(times, content, sender_message.receiver_id)
        user_pic['sender_id'] = sender_message.sender_id
        user_pic['receiver_id'] = sender_message.receiver_id
        time = time_to_str(sender_message.time)
        user_pic['time'] = time
        resp_suc['list'].append(user_pic)


def traverse_collects(results, user_id, resp_suc):
    """
        遍历多条收藏
            collect: 收藏中间表
            resp_suc: 列表
    """
    for result in results:
        collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == result.id).first()
        difference = time_diff(collect.time)
        result_pic = differences(result, difference)
        result_pic.pop('longitude')
        result_pic.pop('latitude')
        pub_picture = PubPicture.query.filter(PubPicture.pub_id == result.id).first()
        county = County.query.filter(County.id == result.county_id).first()
        to_city(result_pic, county)
        if pub_picture:
            if pub_picture.rel_path and pub_picture.pic_name:
                result_pic['pic_path'] = pub_picture.rel_path + '/' + pub_picture.pic_name
        change_latitude_longitude(result_pic, result)
        resp_suc['list'].append(result_pic)


def traverse_collect(result, user_id, resp_suc):
    """
        遍历一条收藏
            collect: 收藏中间表
            resp_suc: 列表
    """
    if result:
        collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == result.id).first()
        difference = time_diff(collect.time)
        result_pic = differences(result, difference)
        result_pic.pop('longitude')
        result_pic.pop('latitude')
        pub_picture = PubPicture.query.filter(PubPicture.pub_id == result.id).first()
        county = County.query.filter(County.id == result.county_id).first()
        to_city(result_pic, county)
        if pub_picture:
            if pub_picture.rel_path and pub_picture.pic_name:
                result_pic['pic_path'] = pub_picture.rel_path + '/' + pub_picture.pic_name
        change_latitude_longitude(result_pic, result)
        resp_suc['list'].append(result_pic)


def to_city(obj_pic, county):
    """
        所在城市
    """
    if county:
        obj_pic['city_county'] = county.name


def system_message_pickler(system_message, resp_suc):
    """
        转换json
    """
    system_message_pic = flatten(system_message)
    resp_suc['system_message_list'].append(system_message_pic)


def direct_message_pickler(direct_message, resp_suc):
    """
        转换json
    """
    direct_message_pic = flatten(direct_message)
    resp_suc['direct_message_list'].append(direct_message_pic)


def traverse_system_message(user_id, resp_suc):
    """
        遍历系统消息
    """
    resp_suc['system_message_list'] = []
    #system_count = db.query(SystemMessage).\
    #    filter(UserSystemMessage.view == 0, UserSystemMessage.user_id == user_id).count()
    user = User.query.filter(User.id == user_id).first()
    system_count = SystemMessage.query.filter(SystemMessage.time > user.system_message_time).count()
    resp_suc['system_count'] = system_count
    if system_count > 1:
        system_messages = SystemMessage.query.filter(SystemMessage.time > user.system_message_time).all()
        return system_messages
    else:
        system_message = SystemMessage.query.filter(SystemMessage.time > user.system_message_time).first()
        return system_message


def traverse_direct_message(user_id, resp_suc):
    """
       私信消息
    """
    message_count = db.query(Message).\
        filter(Message.receiver_id == user_id, Message.view == 0).order_by(Message.time.desc()).\
        group_by(Message.sender_id).count()
    resp_suc['direct_count'] = message_count
    if message_count > 1:
        direct_messages = db.query(Message).\
            filter(Message.receiver_id == user_id, Message.view == 0).order_by(Message.time.desc()).\
            group_by(Message.sender_id).all()
        return direct_messages
    else:
        direct_message = db.query(Message). \
            filter(Message.receiver_id == user_id, Message.view == 0).order_by(Message.time.desc()). \
            group_by(Message.sender_id).first()
        return direct_message


class UserCollect(restful.Resource):
    """
    用户收藏酒吧列表接口
    """
    @staticmethod
    def get():
        """
        所需参数：
            user_id：必传，用户登录的id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'必须要传入user_id。')
        parser.add_argument('page', type=str, required=True, help=u'分页page,传入当前页码')

        args = parser.parse_args()
        user_id = args['user_id']
        page = args['page']
        resp_suc = {}
        resp_suc['list'] = []
        if user_id:
            result_count = db.query(Pub).\
                join(Collect).\
                filter(Collect.user_id == user_id).count()
            temp_page = page
            page, per_page, max = page_utils(result_count, page)
            is_max = max_page(temp_page, max, resp_suc)
            if is_max:
                return resp_suc
            if result_count > 1:
                results = db.query(Pub).\
                    join(Collect).\
                    filter(Collect.user_id == user_id).order_by(Collect.time.desc())[per_page*(page-1):per_page*page]
                traverse_collects(results, user_id, resp_suc)
            else:
                result = db.query(Pub).\
                    join(Collect).\
                    filter(Collect.user_id == user_id).first()
                traverse_collect(result, user_id, resp_suc)
            resp_suc['count'] = result_count
            resp_suc['status'] = 0
        else:
            resp_suc['message'] = 'error'
            resp_suc['status'] = 1

        return resp_suc


class PubCollect(restful.Resource):
    """
    用户收藏酒吧
    """
    @staticmethod
    def get():
        """
        所需参数
            user_id: 必传，登录用户的id
            pub_id: 必传，用户点击收藏的当前酒吧的id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'用户登录user_id必须。')
        parser.add_argument('pub_id', type=str, required=True, help=u'当前酒吧pub_id必须。')

        args = parser.parse_args()
        user_id = args['user_id']
        pub_id = args['pub_id']
        resp_suc = {}
        # 先判断用户是否已经收藏此酒吧
        check_collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == pub_id).count()
        if check_collect >= 1:
            resp_suc['message'] = 'again'
            resp_suc['status'] = 1
        else:
            collect = Collect(user_id=user_id, pub_id=pub_id)
            db.add(collect)
            db.commit()
            resp_suc['message'] = 'success'
            resp_suc['status'] = 0
        return resp_suc


class UserMessage(restful.Resource):
    """
    用户私信接口
    """
    @staticmethod
    def get():
        """
        所需参数:
            user_id: 登录用户id
            page: 分页page，传入当前页
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'用户user_id。')
        parser.add_argument('page', type=str, required=True, help=u'分页page，传入当前页')

        args = parser.parse_args()
        user_id = args['user_id']
        page = args['page']
        resp_suc = {}
        resp_suc['list'] = []
        if user_id:
            message_count = db.query(Message).\
                filter(Message.receiver_id == user_id).group_by(Message.sender_id).count()
            temp_page = page
            page, per_page, max = page_utils(message_count, page)
            is_max = max_page(temp_page, max, resp_suc)
            if is_max:
                return resp_suc
            if message_count > 1:
                # messages = Message.query.filter(Message.receiver_id == user_id, Message.view == 0).order_by
                # (Message.time.desc()).group_by(Message.receiver_id)[per_page*(page-1):per_page*page]
                messages = db.query(Message).\
                    filter(Message.receiver_id == user_id).order_by(Message.time.desc()).\
                    group_by(Message.sender_id)[per_page*(page-1):per_page*page]
                traverse_messages(messages, resp_suc)
            else:
                message = Message.query.filter(Message.receiver_id == user_id).first()
                traverse_message(message, resp_suc)
            resp_suc['status'] = 0
            resp_suc['message'] = 'success'
            return resp_suc
        else:
            resp_suc['status'] = 1
            resp_suc['message'] = 'error'
            return resp_suc


class UserMessageUpdate(restful.Resource):
    """
        用户看过私信修改view值
    """
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('message_id', type=str, required=True, help=u'详细message_id必须。')

        args = parser.parse_args()
        message_id = args['message_id']
        message = Message.query.filter(Message.id == message_id).first()
        message.view = 1
        resp_suc = []

        try:
            db.commit()
            resp_suc['status'] = 0
            resp_suc['message'] = 'success'

        except:
            resp_suc['status'] = 1
            resp_suc['message'] = '未知错误'


class UserMessageInfo(restful.Resource):
    """
        用户私信详细接口
    """
    @staticmethod
    def get():
        """
            参数
            receiver_id: 接受用户id
            sender_id: 发送用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=str, required=True, help=u'sender_id必须')
        parser.add_argument('receiver_id', type=str, required=True, help=u'receiver_id必须')

        args = parser.parse_args()

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['list'] = []

        sender_id = args['sender_id']
        receiver_id = args['receiver_id']

        # message_count = Message.query.filter(Message.sender_id == sender_id).count()
        message_receiver_count = Message.query.filter(Message.sender_id == sender_id, Message.receiver_id == receiver_id).count()
        message_sender_count = Message.query.filter(Message.sender_id == receiver_id, Message.receiver_id == sender_id).count()
        if message_receiver_count > 1:
            # messages = Message.query.filter(Message.sender_id == sender_id).order_by(Message.time.asc())
            if message_sender_count > 1:
                message_senders = Message.query.filter(Message.sender_id == receiver_id, Message.receiver_id == sender_id).\
                    order_by(Message.time)
                traverse_messages_receiver(message_senders, resp_suc)
            else:
                message_senders = Message.query.filter(Message.sender_id == receiver_id, Message.receiver_id == sender_id).first()
                traverse_message_receiver(message_senders, resp_suc)

            message_receivers = Message.query.filter(Message.sender_id == sender_id, Message.receiver_id == receiver_id).\
                order_by(Message.time)
            if message_receivers:
                traverse_messages_receiver(message_receivers, resp_suc)
                return resp_suc
            else:
                return resp_fail
        else:
            # message = Message.query.filter(Message.sender_id == sender_id).first()
            message_receiver = Message.query.filter\
                    (Message.sender_id == sender_id, Message.receiver_id == receiver_id).first()
            if message_receiver:
                traverse_message_receiver(message_receiver, resp_suc)
                return resp_suc
            else:
                return resp_fail


class UserSenderMessage(restful.Resource):
    """
        用户发送私信
    """
    @staticmethod
    def get():
        """
            参数:
                sender_id:发送的id
                receiver_id:接收的id
                content: 发送内容
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=str, required=True, help=u'sender_id必须。')
        parser.add_argument('receiver_id', type=str, required=True, help=u'receiver_id必须。')
        parser.add_argument('content', type=str, required=True, help=u'content必须。')
        # parser.add_argument('date', type=str, required=True, help=u'date必须.')

        args = parser.parse_args()
        sender_id = args['sender_id']
        receiver_id = args['receiver_id']
        content = args['content']
        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['sender_list'] = []

        if sender_id == receiver_id:
            resp_fail['message'] = '您不能发给自己！'
            return resp_fail

        message = Message(sender_id, receiver_id, content, view=0)
        db.add(message)
        try:
            db.commit()
        except:
            return resp_fail
        message = Message.query.filter(Message.id == message.id).first()
        traverse_message_sender(message, resp_suc)
        return resp_suc


class MessageFuck(restful.Resource):
    """
        消息，系统消息，私信消息。
    """
    @staticmethod
    def get():
        """
            参数
                user_id:用户登录id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id必须。')

        args = parser.parse_args()

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['sender_list'] = []
        resp_suc['system_message_list'] = []
        user_id = args['user_id']
        system_message = traverse_system_message(user_id, resp_suc)
        direct_message = traverse_direct_message(user_id, resp_suc)
        if system_message or direct_message:
            #if type(system_message) is list:
            #    for system in system_message:
            #        system_message_pickler(system, resp_suc)
            #else:
            #    system_message_pickler(system_message, resp_suc)
            #if type(direct_message) is list:
            #    for direct in direct_message:
            #        traverse_messages_sender(direct, resp_suc)
            #else:
            #    traverse_message_sender(direct_message, resp_suc)
            return resp_suc
        else:
            return resp_fail


class MessageByTypeInfo(restful.Resource):
    '''根据消息类型进入详情'''
    @staticmethod
    def get():
        """
        参数，
           type: 详细类型
           user_id: 用户登录id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('types', type=str, required=True, help=u'type选择信息类型,0:系统，1私信')
        parser.add_argument('user_id', type=str, required=True, help=u'user_id。用户登陆id')

        args = parser.parse_args()

        types = args['types']
        user_id = args['user_id']
        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic
        resp_suc['sender_list'] = []

        system_message = traverse_system_message(user_id, resp_suc)
        direct_message = traverse_direct_message(user_id, resp_suc)
        if types == '0':
            user = User.query.filter(User.id == user_id).first()
            if type(system_message) is list:
                for system in system_message:
                    system_message_pickler(system, resp_suc)
                    user.system_message_time = todayfstr()
                    db.commit()
            else:
                if system_message:
                    system_message_pickler(system_message, resp_suc)
                    user.system_message_time = todayfstr()
                    db.commit()
        else:
            if type(direct_message) is list:
                traverse_messages_sender(direct_message, resp_suc)
            else:
                traverse_message_sender(direct_message, resp_suc)
        return resp_suc


class ClearMessage(restful.Resource):
    """
        清除私信
    """
    @staticmethod
    def get():
        """
            参数：
                user_id：用户登录id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'user_id必须.')

        args = parser.parse_args()

        user_id = args['user_id']

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic

        message_count = Message.query.filter(Message.receiver_id == user_id).count()
        if message_count > 1:
            messages = Message.query.filter(Message.receiver_id == user_id).all()
            for message in messages:
                db.delete(message)
                try:
                    db.commit()
                except:
                    return resp_fail
            return resp_suc
        else:
            message = Message.query.filter(Message.receiver_id == user_id).first()
            db.delete(message)
            try:
                db.commit()
            except:
                return resp_fail
            return resp_suc


class FeedBackAdd(restful.Resource):
    """
        意见反馈
    """
    @staticmethod
    def get():
        """
            参数
                content: 反馈内容
                user_id: 登录用户id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True, help=u'content必须。')
        parser.add_argument('user_id', type=str, required=True, help=u'user_id必须。')

        args = parser.parse_args()

        resp_suc = success_dic().dic
        resp_fail = fail_dic().dic

        content = args['content']
        user_id = args['user_id']
        feed_back = FeedBack(content=content, user_id=user_id)

        try:
            db.add(feed_back)
            db.commit()
        except:
            return resp_fail
        return resp_suc
