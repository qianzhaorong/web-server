import time

class Utils:
    @staticmethod
    def log(*args, **kwargs):
        """log来代替print函数，打印日志"""
        unix_time = int(time.time())
        format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_time))
        print(format_time, *args, **kwargs)