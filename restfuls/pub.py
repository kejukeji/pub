# coding: utf-8

from flask.ext import restful
from models import Pub, PubType, PubTypeMid, PubPicture
from utils import pickler
from flask.ext.restful import reqparse


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
            pub_type_pic = pickler.flatten(pub_type)
            resp_suc['list'].append(pub_type_pic)
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
            type_id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('type_id', type=str, required=True)

        args = parser.parse_args()
        resp_suc = {}
        resp_suc['list'] = []
        if args['type_id']:
            pub_type_count = PubTypeMid.query.filter(PubTypeMid.pub_type_id == int(args['type_id'])).count()
            if pub_type_count > 1:
                pub_types = PubTypeMid.query.filter(PubTypeMid.pub_type_id == int(args['type_id']))
                for pub_type in pub_types:
                    pub_count = Pub.query.filter(Pub.id == pub_type.pub_id).count()
                    if pub_count > 1:
                        pubs = Pub.query.filter(Pub.id == pub_type.pub_id)
                        for pub in pubs:
                            pub_pic = pickler.flatten(pub)
                            pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub.id).first()
                            pub_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
                            resp_suc['list'].append(pub_pic)
                    else:
                        pub = Pub.query.filter(Pub.id == pub_type.pub_id).first()
                        pub_pic = pickler.flatten(pub)
                        pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub.id).first()
                        pub_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
                        resp_suc['list'].append(pub_pic)
            else:
                pub_type = PubTypeMid.query.filter(PubTypeMid.pub_type_id == int(args['type_id'])).first()
                pub = Pub.query.filter(Pub.id == pub_type.pub_id).first()
                pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub.id).first()
                pub_pic = pickler.flatten(pub)
                pub_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
                resp_suc['list'].append(pub_pic)
            resp_suc['status'] = 0
            return resp_suc
        else:
            resp_suc['message'] = 'error'
            resp_suc['status'] = 1
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
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pub_id', type=str, required=True)
        args = parser.parse_args()
        resp_suc = {}
        resp_suc['picture_list'] = []
        resp_suc['pub_list'] = []
        pub_id = int(args['pub_id'])
        if pub_id:
            pub = Pub.query.filter(Pub.id == pub_id).first()
            pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub_id).first()
            pub_pic = pickler.flatten(pub)
            pub_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
            resp_suc['pub_list'].append(pub_pic)
            pub_p_count = PubPicture.query.filter(PubPicture.pub_id == pub.id).count()
            if pub_p_count > 1:
                pub_ps = PubPicture.query.filter(PubPicture.pub_id == pub_id)
                for pub_picture in pub_ps:
                    pub_picture_pic = pickler.flatten(pub_picture)
                    pub_picture_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
                    resp_suc['picture_list'].append(pub_picture_pic)
            else:
                pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub_id).first()
                pub_picture_pic = pickler.flatten(pub_picture)
                pub_picture_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
                resp_suc['picture_list'].append(pub_picture_pic)
            resp_suc['status'] = 0
            return resp_suc
        else:
            resp_suc['status'] = 1
            resp_suc['message'] = 'error'
            return resp_suc