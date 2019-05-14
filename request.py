class Request:
    def __init__(self, method, path, query, headers, body):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
    
    def __str__(self):
        return "Request【请求方法：{}, 请求路径：{}，请求参数：{}，请求体：{}】".format(self.method, self.path, self.query, self.body)