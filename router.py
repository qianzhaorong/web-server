# coding:utf-8
"""
读取urls.py文件中的路由映射，调用相应的处理函数
[
    (r'/', index, name='index')
]
"""
from urls import urls
from views import *


class Router:
    def __init__(self, request):
        self.request = request

    def get_response(self):
        path = self.request.path
        callback = urls.get(path, self.route_404)
        return callback(self.request)

    def route_404(self, request):
        return Response("404", "Not Found", "")
