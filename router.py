# coding:utf-8


def route_index(request):
    """主页的处理函数，读取主页的html文件，构造HTTP报文返回"""
    pass


def route(request):
    """接收一个Request对象，进行路由转发"""
    r = {
        '/static': route_static,
        '/': route_index,
        '/login': route_login,
        '/register': route_register,
    }
    route_handle = r.get(request.path, error_404)
    return route_handle(request)