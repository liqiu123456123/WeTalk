# chat/routing.py

# 导入 Django 的 URL 路由模块中的 re_path 函数，该函数用于基于正则表达式的 URL 路由匹配。
from django.urls import re_path

# 从当前目录下的 consumers 模块中导入 ChatConsumer 类，这个类通常定义了 WebSocket 相关的逻辑。
from . import consumers

# 定义一个名为 websocket_urlpatterns 的列表，用于存放 WebSocket 的路由规则。
websocket_urlpatterns = [
    # 使用 re_path 函数定义一个 WebSocket 路由规则，匹配以 "ws/chat/" 开头，后面跟着一个或多个单词字符（\w+）作为房间名的 URL。
    # 捕获的房间名会被传递给 ChatConsumer 类的实例方法，作为参数 `room_name`。
    # ChatConsumer.as_asgi() 将 ChatConsumer 转换为一个 ASGI 应用，这是 Django Channels 用于处理 WebSocket 通信的方式。
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]