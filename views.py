from response import Response
"""
编写视图函数
"""

def route_index(request):
    return Response("200", "Very OK", "")
