# coding:utf-8
import socket
import urllib.parse
import threading

from utils import Utils
from request import Request
from router import Router

BUFFER = 1024   


class Server:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen(5)
            Utils.log("---服务器启动在：{}:{}---".format(self.host, self.port))
            
            while True:
                conn, address = s.accept()
                Utils.log("---客户：{}:{} 连接---".format(address[0], address[1]))

                # 获取请求数据
                request_data = self.get_request_data(conn)
                
                # 根据数据解析得到Request对象
                request = self.parse_data(request_data)
                Utils.log(request)

                # 将request对象交给视图函数，视图函数需要返回Response对象
                response = Router(request).get_response()
                # 将response对象组装成返回报文
                send_data = self.build_response(response)

                conn.send(send_data.encode("utf-8"))
                conn.close()

    def get_request_data(self, conn):
        """获取请求数据"""
        data = b''
        while True:
            d = conn.recv(BUFFER)
            if len(d) < BUFFER:
                data += d
                break
        
        return data.decode("utf-8")

    def parse_data(self, data):
        """解析数据，返回Request对象"""
        method = ''
        path = ''
        query = {}
        headers = {}
        body = {}

        method = self.parse_method(data)
        path = self.parse_path(data)
        query = self.parse_query(data)
        headers = self.parse_headers(data)
        body = self.parse_body(data)


        return Request(method, path, query, headers, body)

    def get_request_line(self, data):
        return data.split("\r\n")[0]

    def parse_method(self, data):
        """解析出请求方法"""
        request_line = self.get_request_line(data)

        return request_line.split(" ")[0]

    def parse_path(self, data):
        """解析出请求路径"""
        request_line = self.get_request_line(data)

        # /index?page=1
        string = request_line.split(" ")[1]
        path = string.split("?")[0]
        return path

    def parse_query(self, data):
        """解析出请求参数"""
        query = {}

        request_line = self.get_request_line(data)
        # /index?page=1&status=2
        string = request_line.split(" ")[1]
        arr = string.split("?")
        if len(arr) > 1 :
            query_string = arr[1]
            # 再以&分割
            for item in query_string.split("&"):
                query[item.split("=")[0]] = item.split("=")[1]
        return query

    def parse_headers(self, data):
        """
        解析出headers
        Connection:keep-alive\r\n
        Host:baidu.com\r\n
        """
        headers = {}

        request_headers = data.split("\r\n\r\n")[0].split("\r\n")[1:]
        if request_headers:
            for item in request_headers:
                key = item.split(":")[0]
                value = item.split(":")[1]
                headers[key] = value

        return headers

    def parse_body(self, data):
        """
        解析body
        a=1&b=2
        """
        body = {}

        request_body = data.split("\r\n\r\n")[1]
        if request_body:
            for item in request_body.split("&"):
                key = item.split("=")[0]
                value = item.split("=")[1]
                body[key] = value

        return body

    def build_response(self, response):
        """
        组装response
        HTTP/1.1 200 OK
        """
        response_line = "HTTP/1.1 " + response.status_code + " " + response.status_reason 

        response_headers = ""
        for key, value in response.headers.items():
            response_headers = response_headers + key + "=" + value + "\r\n"
        
        return response_line + "\r\n" + response_headers + "\r\n" + response.body



if __name__ == "__main__":
    server = Server(port=3000)
    server.start()