# import json
# from django.contrib.auth.models import User  # 导入Django的用户模型
# from .models import ChatMessage  # 导入自定义的ChatMessage模型
# from channels.generic.websocket import AsyncWebsocketConsumer  # 导入Django Channels的异步Websocket消费者基类
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     # WebSocket连接建立时的处理函数
#     async def connect(self):
#         # 从URL路由中获取接收者的ID和房间名
#         self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         # 构建房间组的名称，假设格式为"chat_{room_name}"
#         self.room_group_name = f"chat_{self.room_name}"
#
#         # 将当前消费者加入到房间组中，以便接收和发送消息
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#
#         # 接受WebSocket连接
#         await self.accept()
#
#         # WebSocket连接关闭时的处理函数
#
#     async def disconnect(self, close_code):
#         # 从房间组中移除当前消费者
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#
#         # 接收从WebSocket发送过来的消息的处理函数
#
#     async def receive(self, text_data):
#         # 将接收到的文本数据解析为JSON格式
#         text_data_json = json.loads(text_data)
#         # 从JSON中提取发送者ID和消息内容
#         sender_id = text_data_json.get('sender_id')
#         message = text_data_json.get('message')
#
#         # 验证接收到的数据是否有效
#         if sender_id and message:
#             # 在数据库中创建ChatMessage实例
#             chat_message = ChatMessage.objects.create(
#                 sender_id=sender_id,  # 发送者ID
#                 receiver_id=self.receiver_id,  # 接收者ID
#                 content=message  # 消息内容
#             )
#
#             # 将消息发送到房间组，以便其他消费者也能接收到
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat.message',  # 消息类型
#                     'message': {
#                         'sender_id': sender_id,  # 发送者ID
#                         'content': message  # 消息内容
#                     }
#                 }
#             )
#
#             # 从房间组接收消息的处理函数
#
#     async def chat_message(self, event):
#         # 从事件中获取消息内容
#         message_data = event['message']
#         sender_id = message_data['sender_id']  # 发送者ID
#         content = message_data['content']  # 消息内容
#
#         # 可选：如果需要，从数据库中获取发送者User对象
#         # sender = User.objects.get(id=sender_id)
#
#         # 将消息发送到WebSocket连接
#         await self.send(text_data=json.dumps({
#             'sender_id': sender_id,  # 发送者ID
#             'content': content  # 消息内容
#         }))


# 导入所需的库和模块
import json  # 导入json库，用于处理JSON数据
from channels.generic.websocket import AsyncWebsocketConsumer  # 导入异步WebSocket消费者基类
from .models import ChatMessage
from account.models import MyUser

# 定义一个名为ChatConsumer的类，它继承自AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):

    # 当WebSocket连接建立时调用的异步方法
    async def connect(self):
        # 从scope中获取房间名（room_name），这通常是从URL路由参数中获取的
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # 根据房间名构造一个房间组名（room_group_name），这样可以将多个WebSocket连接组织在同一个房间中
        self.room_group_name = f"chat_{self.room_name}"

        # 将当前的WebSocket连接（channel_name）加入到房间组（room_group_name）中
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # 接受WebSocket连接
        await self.accept()

        # 当WebSocket连接断开时调用的异步方法

    async def disconnect(self, close_code):
        # 将当前的WebSocket连接（channel_name）从房间组（room_group_name）中移除
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # 当从WebSocket接收到消息时调用的异步方法

    async def receive(self, text_data):
        # 将接收到的文本数据解析为JSON格式
        text_data_json = json.loads(text_data)
        # 从JSON中提取消息内容
        message = text_data_json["message"]
        sender_username = text_data_json["sender_username"]
        receiver_username = text_data_json["receiver_username"]

        user = MyUser.objects.get(username=sender_username)
        # 获取用户的id
        sender_id = user.id

        user = MyUser.objects.get(username=receiver_username)
        # 获取用户的id
        receiver_id = user.id

        print("message", message)
        # 创建ChatMessage实例并保存到数据库
        chat_message = ChatMessage(content=message, sender_id=sender_id,
                                   receiver_id=receiver_id)  # 假设ChatMessage有一个content字段
        chat_message.save()  # 保存消息到数据库
        # 将消息发送到房间组，这样所有在该房间组中的WebSocket连接都可以接收到这个消息
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

        # 当从房间组接收到消息时调用的异步方法

    async def chat_message(self, event):
        # 从事件中提取消息内容
        message = event["message"]

        # 将消息发送到WebSocket连接
        await self.send(text_data=json.dumps({"message": message}))
