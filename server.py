# coding:utf-8
import socket
import time
import urllib.parse

def log(*args, **kwargs):
    """log来代替print函数，打印日志"""
    unix_time = int(time.time())
    format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_time))
    print(format_time, *args, **kwargs)


def get_request_data(connection): 
    """根据connection来获取客户端发送的请求数据"""
    data = b''
    buffer_size = 1024
    while True: 
        d = connection.recv(buffer_size)
        data += d
        if(len(d) < buffer_size):
            break
    return data.decode("utf-8")


class Request(object):
    def __init__(self, method, path, query, headers, cookies, body):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.cookies = cookies
        self.body = body

    def __repr__(self):
        return "【请求方法：{}， 请求路径：{}， 请求参数：{}】".format(self.method, self.path, self.query)


def parse_headers_cookies(request_data):
    """根据HTTP请求报文解析出headers和cookies
    例子：Connection: keep-alive
          Host: localhost:3000
          Cookie:username=q
    返回：headers = {
        'Connection': 'keep-alive',
        'Host': 'localhost:3000',
        'Cookie': 'username=q',
        }
        cookies = {
            'username': 'q',
        }
    """
    headers = {}
    cookies = {}

    # 通过HTTP报文中的\r\n来分割
    headers_list = request_data.split("\r\n\r\n")[0].split("\r\n")[1:]
    for h in headers_list:
        key = h.split(":", 1)[0]
        value = h.split(":", 1)[1]
        headers[key] = value
    # 通过解析出来的headers判断是否有cookies字段
    cookies_str = headers.get("Cookie", "")
    if cookies_str != "":
        for c in cookies_str.split(";"):
            c_key = c.split("=", 1)[0]
            c_value = c.split("=", 1)[1]
            cookies[c_key] = c_value

    return headers, cookies


def parse_method_path_query(request_data):
    """根据HTTP请求报文解析出 请求方法、请求路径和请求参数
    例：GET /index?a=1&b=2 HTTP/1.1
    返回：
        method: GET
        path: /index
        query: {
            'a': '1',
            'b': '2',
        }
    """
    method = 'GET'
    path = '/'
    query = {}

    request_line = request_data.split("\r\n")[0]
    method = request_line.split(" ")[0]
    path_and_query = request_line.split(" ")[1]
    # 再解析路径和请求参数，路径和参数通过?分割
    if '?' in path_and_query:
        path = path_and_query.split("?")[0]
        raw_query = path_and_query.split("?")[1]
        # 解析得到的raw_query可能会有经过编码的中文，所以需要先解码
        if raw_query is not None:
            # 此时的key_value是一个数组，类似于['a=1', 'b=2']这种，此时遍历这个数组，再通过切割字符串组成query字典
            key_value = urllib.parse.unquote(raw_query).split("&")
            for i in key_value:
                query[i.split("=")[0]] = i.split("=")[1]

    return method, path, query


def parse_body(request_data):
    """根据HTTP请求报文解析出body
    例：
        POST /index HTTP/1.1
        Host: localhost:3000

        username=q&password=123
    此时需要将HTTP报文中的body解析成字典
    """
    body = {}
    body_str = request_data.split("\r\n\r\n")[1]
    if body_str != "":
        for b in body_str.split("&"):
            b_key = b.split("=", 1)[0]
            b_value = b.split("=", 1)[1]
            body[b_key] = b_value

    return body


def run(host, port):
    """启动web server"""
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        log("**服务器启动在： {}端口**".format(str(port)))
        while True:
            connection, address = s.accept()
            log("客户端地址：", address)
            # 等待客户发送请求，并得到HTTP请求报文
            request_data = get_request_data(connection)
            log("请求报文：", request_data)
            # 解析客户端的请求报文，得到各个字段
            method, path, query = parse_method_path_query(request_data)
            headers, cookies = parse_headers_cookies(request_data)
            body = parse_body(request_data)
            # 封装成request对象
            request = Request(method, path, query, headers, cookies, body)
            log("request对象：", request)
            # 进行路由转发，得到返回数据

            # 最后需要得到一个返回报文，通过connection对象返回给客户端
            response_data = ""
            connection.send(response_data.encode("utf-8"))
            connection.close()



def main(host='localhost', port=3000):
    run(host, port)


if __name__ == "__main__":
    config = {
        'host': 'localhost',
        'port': 3000,
    }
    main(**config)