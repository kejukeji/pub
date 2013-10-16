# coding: utf-8

from flask.ext import restful
from models import Pub, PubType, PubTypeMid, PubPicture, engine
from utils import pickler
from flask.ext.restful import reqparse
from sqlalchemy.orm import Session, sessionmaker


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
        parser.add_argument('type_id', type=str, required=True, help=u'酒吧类型type_id必须。')

        args = parser.parse_args()
        resp_suc = {}
        resp_suc['list'] = []
        resp_suc['hot_list'] = []
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        if args['type_id']:
            result_count = session.query(PubPicture).\
                join(Pub).\
                join(PubTypeMid).\
                filter(PubTypeMid.pub_type_id == int(args['type_id']), Pub.recommend == 1).\
                group_by(PubPicture.pub_id).count()
            if result_count > 1:
                results = session.query(PubPicture). \
                    join(Pub). \
                    join(PubTypeMid).\
                    filter(PubTypeMid.pub_type_id == int(args['type_id']), Pub.recommend == 1).\
                    group_by(PubPicture.pub_id)
                for result in results:
                    if result:
                        result_pic = pickler.flatten(result)
                        result_pic['pic_path'] = result.rel_path + result.pic_name
                        resp_suc['hot_list'].append(result_pic)
            else:
                result = session.query(PubPicture). \
                    join(Pub). \
                    join(PubTypeMid).\
                    filter(PubTypeMid.pub_type_id == int(args['type_id']), Pub.recommend == 1).\
                    group_by(PubPicture.pub_id).first()
                if result:
                    result_pic = pickler.flatten(result)
                    result_pic['pic_path'] = result.rel_path + result.pic_name
                    resp_suc['hot_list'].append(result_pic)

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
        parser.add_argument('pub_id', type=str, required=True, help=u'酒吧pub_id必须。')
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
            resp_suc['message'] = 'success'
            return resp_suc
        else:
            resp_suc['status'] = 1
            resp_suc['message'] = 'error'
            return resp_suc


class PubPictureDetail(restful.Resource):
    """
    酒吧图片列表
    """
    @staticmethod
    def get():
        """
        所需参数:
            pub_id:必传，所点击图片的当前酒吧id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('pub_id', type=str, required=True, help=u'酒吧pub_id必须。')

        args = parser.parse_args()
        resp_suc = {}
        resp_suc['list'] = []
        if args['pub_id']:
            pub_id = int(args['pub_id'])
            pub_picture_count = PubPicture.query.filter(PubPicture.pub_id == pub_id).count()
            if pub_picture_count > 1:
                pub_pictures = PubPicture.query.filter(PubPicture.pub_id == pub_id)
                for pub_picture in pub_pictures:
                    pub_picture_pic = pickler.flatten(pub_picture)
                    pub_picture_pic['pic_path'] = pub_picture.rel_path + pub_picture.pic_name
                    resp_suc['list'].append(pub_picture_pic)
            else:
                pub_picture = PubPicture.query.filter(PubPicture.pub_id == pub_id).first()
                pub_picture_pic = pickler.flatten(pub_picture)
                resp_suc['list'].append(pub_picture_pic)
        else:
            resp_suc['message'] = 'error'
            resp_suc['status'] = 1

        return resp_suc


class PubSearch(restful.Resource):
    """
    搜索酒吧
    """
    @staticmethod
    def get():
        """
        所需参数:
            content:搜索酒吧内容
        """
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True, help=u'content必须，搜索酒吧')

        args = parser.parse_args()
        resp_suc = {}
        resp_suc['pub_list'] = []
        resp_suc['pub_picture_list'] = []
        if args['content']:
            content = str(unicode(args['content']))
            s = '%' + content + '%'
            sql = "select a.*,b.rel_path,b.pic_name from pub a " \
                  "inner join pub_picture b on a.id = b.pub_id " \
                  "where a.name like '" + s + "''"
            results = engine.execute(sql)
            for result in results:
                print "user_name:", result['a.name']




