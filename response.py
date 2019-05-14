class Response:
    def __init__(self, status_code, status_reason, body):
        self.status_code = status_code
        self.status_reason = status_reason
        self.body = body
        self.headers = {
            'Context-Type': 'text/html',
        }

    def set_headers(self, headers):
        self.headers.update(headers)
        
    def set_status_code(self, code):
        self.status_code = code
    
    def set_status_reason(self, reason):
        self.reason = reason