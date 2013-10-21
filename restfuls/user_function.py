# coding: utf-8

from flask.ext import restful
from sqlalchemy.orm import Session, sessionmaker
from models import Collect, Pub, User, engine, db, Message, UserInfo
from flask.ext.restful import reqparse
from utils import pickler, time_diff
from datetime import datetime


def differences(obj, time_dif):
    """
    计算时间差
    """
    obj_pic = pickler.flatten(obj)
    obj_pic['difference'] = time_dif
    return obj_pic


def get_year(time):
    dt = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
    today = datetime.today()
    s = int((today - dt).total_seconds())
    return str(s / 3600 / 24 / 365)


def to_messages(times, content, message_id):
    """
    用户发送时间times
    用户发送内容content
    """
    user = User.query.filter(User.id == message_id).first()
    user_info = UserInfo.query.filter(UserInfo.user_id == user.id).first()
    if user_info:
        sex = user_info.sex
        birthday = user_info.birthday
        age = get_year(birthday)
        json_pic = pickler._flatten(user)
        if sex == 1:
            json_pic['sex'] = '男'
        else:
            json_pic['sex'] = '女'
        json_pic['age'] = age
    json_pic['send_time'] = times
    json_pic['content'] = content
    return json_pic


def traverse_messages(messages, resp_suc):
    """
        遍历多条消息
    """
    if messages:
        for message in messages:
            times = time_diff(message.time)
            content = message.content
            user_pic = to_messages(times, content, message.sender_id)
            resp_suc['list'].append(user_pic)


def traverse_message(message, resp_suc):
    """
        遍历一条消息
    """
    if message:
        times = time_diff(message.time)
        content = message.content
        user_pic = to_messages(times, content, message.sender_id)
        resp_suc['list'].append(user_pic)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class UserCollect(restful.Resource):
    """
    用户收藏酒吧列表接口
    """
    @staticmethod
    def get():
        """
        所需参数：
            user_id：必传，用户登录的id
            pub_id: 必传,用户收藏的酒吧id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help=u'必须要传入user_id。')

        args = parser.parse_args()
        user_id = int(args['user_id'])

        resp_suc = {}
        resp_suc['list'] = []
        if user_id:
            result_count = session.query(Pub).\
                join(Collect).\
                filter(Collect.user_id == user_id).count()

            if result_count > 1:
                results = session.query(Pub).\
                    join(Collect).\
                    filter(Collect.user_id == user_id)
                for result in results:
                    collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == result.id).first()
                    difference = time_diff(collect.time)
                    result_pic = differences(result, difference)
                    resp_suc['list'].append(result_pic)
            else:
                result = session.query(Pub).\
                    join(Collect).\
                    filter(Collect.user_id == user_id).first()
                if result:
                    collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == result.id)
                    difference = time_diff(collect.time)
                    result_pic = differences(result, difference)
                    resp_suc['list'].append(result_pic)
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
        user_id = int(args['user_id'])
        pub_id = int(args['pub_id'])
        resp_suc = {}
        # 先判断用户是否已经收藏此酒吧
        check_collect = Collect.query.filter(Collect.user_id == user_id, Collect.pub_id == pub_id).count()
        if check_collect >= 1:
            resp_suc['message'] = 'again'
            resp_suc['status'] = 2
        else:
            collect = Collect(user_id, pub_id)
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
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True)

        args = parser.parse_args()
        user_id = args['user_id']
        resp_suc = {}
        resp_suc['list'] = []
        if user_id:
            message_count = Message.query.filter(Message.receiver_id == user_id).count()
            if message_count > 1:
                messages = Message.query.filter(Message.receiver_id == user_id)
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