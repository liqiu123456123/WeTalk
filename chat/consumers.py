# 导入所需的库和模块
import base64
import numpy as np
import cv2
import json  # 导入json库，用于处理JSON数据
from channels.generic.websocket import AsyncWebsocketConsumer  # 导入异步WebSocket消费者基类
from .models import ChatMessage
from account.models import MyUser
from datetime import datetime


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
        try:
            text_data_json = json.loads(text_data)
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
            # 获取当前时间
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", "message": message, "sender_username": sender_username,
                 "receiver_username": receiver_username}
            )
        except:
            data = json.loads(text_data)
            image_data = data.get('image', None)
            unique_id = data.get('id', None)

            if image_data and unique_id:
                # 去掉Base64编码字符串的前缀（例如"data:image/png;base64,"）
                image_base64 = image_data.split(',')[1]

                # 解码Base64字符串为字节
                imm = base64.b64decode(image_base64)

                # 将字节转换为numpy数组
                im_np = np.asarray(bytearray(imm), dtype="uint8")

                # 根据图像数据解码图像
                im = cv2.imdecode(np.frombuffer(im_np, np.uint8), cv2.IMREAD_COLOR)

                # 使用唯一ID作为窗口名称
                window_name = f'Video Stream {unique_id}'

                # 显示图像
                cv2.imshow(window_name, im)

                # 等待按键，如果需要的话，可以调整等待时间或者使用其他逻辑来控制窗口的关闭
                cv2.waitKey(1)
            else:
                print("Incomplete data received")
                # 从JSON中提取消息内容

        # 当从房间组接收到消息时调用的异步方法

    async def chat_message(self, event):
        # 从事件中提取消息内容
        message = event["message"]
        sender_username = event["sender_username"]
        receiver_username = event["receiver_username"]
        print(event)
        # 将消息发送到WebSocket连接
        await self.send(text_data=json.dumps(
            {"message": message, "sender_username": sender_username, "receiver_username": receiver_username}))
