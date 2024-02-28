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
        # 区分视频和语音
            data = json.loads(text_data)
            self.type = data.get('type', None)
            if self.type == "video":
                image_data = data.get('image', None)
                unique_id = data.get('id', None)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat.message", "video_message": image_data, "id": unique_id})

            else:
                audio_data = data.get('audio')
                unique_id = data.get('id', None)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat.message", "audio_message": audio_data, "id": unique_id})
        # 当从房间组接收到消息时调用的异步方法

    async def chat_message(self, event):
        # 从事件中提取消息内容
        try:
            # 简单区分图像和文字
            message = event["message"]
            sender_username = event["sender_username"]
            receiver_username = event["receiver_username"]
            # 将消息发送到WebSocket连接
            await self.send(text_data=json.dumps(
                {"message": message, "sender_username": sender_username, "receiver_username": receiver_username}))
        except:
            if self.type == "video":
                message = event["video_message"]
                uid = event["id"]
                # 将消息发送到WebSocket连接
                await self.send(text_data=json.dumps(
                    {"message": message, "uid": uid}))
            else:
                message = event["audio_message"]
                import base64
                import pyaudio
                chunk = 4096  # Record in chunks of 1024 samples
                sample_format = pyaudio.paInt16  # 16 bits per sample
                channels = 2  # 两声道
                fs = 44100  # Record at 44100 samples per second
                p = pyaudio.PyAudio()  # 创建音频对象
                micstream = p.open(format=sample_format,  # 音频输入流创建
                                   channels=channels,
                                   rate=fs,
                                   frames_per_buffer=chunk,
                                   input=True)

                decoded_bytes = base64.b64decode(message)
                y = []
                for i in range(15):
                    m = micstream.read(chunk)
                    y.append(m)
                # 将所有的字节数据连接成一个字节串
                audio_bytes = b''.join(y)
                # 将字节数据转换为 Base64 编码的字符串
                base64_audio = base64.b64encode(audio_bytes).decode('utf-8')

                uid = event["id"]
                # 将消息发送到WebSocket连接
                if len(message) > 1: await self.send(bytes_data=audio_bytes)
