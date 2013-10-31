# coding: utf-8

"""无法分离为通用函数的视图函数处理库"""

import Image

from models import Pub, PubPicture, db
from utils import time_file_name


def save_thumbnail(picture_id):
    """通过图片ID，查找图片，生产略缩图，存储本地，然后存储数据库"""

    pub_picture = PubPicture.query.filter(PubPicture.id == picture_id).first()
    save_path = pub_picture.base_path + pub_picture.rel_path + '/'
    picture = save_path + pub_picture.pic_name
    im = Image.open(picture)
    thumbnail = im.thumbnail((256, 256))
    thumbnail_name = time_file_name(pub_picture.upload_name, sign='nail') + '.jpeg'
    thumbnail.save(save_path+thumbnail_name, 'jpeg')
    pub_picture.thumbnail = thumbnail_name
    db.commit()
