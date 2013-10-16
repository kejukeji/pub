# coding: utf-8

from flask.ext import restful
from sqlalchemy.orm import Session, sessionmaker
from models import Collect, Pub, User, engine, db
from flask.ext.restful import reqparse
from utils import pickler


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

        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

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
                    result_pic = pickler.flatten(result)
                    resp_suc['list'].append(result_pic)
            else:
                result = session.query(Pub).\
                    join(Collect).\
                    filter(Collect.user_id == user_id).first()
                result_pic = pickler.flatten(result)
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
        resp_suc['list'] = []
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
