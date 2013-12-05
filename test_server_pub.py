# coding: utf-8

"""这个文件的功能是提高可配置，如果用于测试，运行这个文件比较好"""

from pub_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6001)
