# coding: utf-8

from pub_app import app

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(7071)  # flask默认的端口,可任意修改
IOLoop.instance().start()