# coding: utf-8

import datetime


def allowed_file(filename, allowed_extension):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extension


def time_file_name(filename):
    return str(datetime.datetime.now()).replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')\
           + filename