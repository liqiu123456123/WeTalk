# 导入操作系统模块，用于设置环境变量
import os

# 从channels.auth导入AuthMiddlewareStack，这是一个中间件堆栈，用于处理WebSocket认证
from channels.auth import AuthMiddlewareStack

# 从channels.routing导入ProtocolTypeRouter和URLRouter，这两个是用于处理不同协议类型请求的路由器
from channels.routing import ProtocolTypeRouter, URLRouter

# 从channels.security.websocket导入AllowedHostsOriginValidator，这是一个验证器，用于验证WebSocket连接的来源主机是否允许
from channels.security.websocket import AllowedHostsOriginValidator

# 从django.core.asgi导入get_asgi_application，用于获取Django的ASGI应用实例
from django.core.asgi import get_asgi_application

# 从chat.routing导入websocket_urlpatterns，这是WebSocket的URL模式列表
from chat.routing import websocket_urlpatterns

# 设置环境变量"DJANGO_SETTINGS_MODULE"的默认值为"WeTalk.settings"，这是Django项目的设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeTalk.settings")

# 提前初始化Django的ASGI应用实例，以确保在应用注册中心（AppRegistry）被填充之前，
# 导入可能使用ORM模型的代码。这是为了避免在导入模型时可能出现的Django尚未准备好的问题。
django_asgi_app = get_asgi_application()

# 再次导入chat.routing模块，虽然这在上面的代码中已经完成了，但这里可能是为了确保在后续代码中能够访问该模块。
import chat.routing

# 定义一个名为application的ProtocolTypeRouter实例，它根据请求的协议类型来分发请求。
# 对于HTTP请求，它使用上面初始化的Django ASGI应用实例(django_asgi_app)来处理。
# 对于WebSocket请求，它使用一个包含认证中间件堆栈和URL路由器的结构来处理，
# 其中认证中间件堆栈确保WebSocket连接经过认证，URL路由器则根据websocket_urlpatterns来路由请求。
# AllowedHostsOriginValidator用于验证WebSocket连接的来源主机。
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)