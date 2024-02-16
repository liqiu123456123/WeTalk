# 导入异步I/O库，用于支持并发操作
import asyncio

# 导入base64库，用于对捕获的图像进行base64编码
import base64

# 导入BytesIO类，用于处理二进制数据
from io import BytesIO

# 导入OpenCV库，用于视频捕获和图像处理
import cv2

# 导入NumPy库，用于进行数值计算
import numpy as np

# 从PIL库导入Image模块，用于图像处理和格式转换
from PIL import Image

# 导入websockets库，用于建立WebSocket连接
import websockets

# WebSocket服务器的地址和端口
WEBSOCKET_URI = 'ws://192.168.60.105:8765'


# 定义一个异步函数，用于捕获视频并发送到WebSocket服务器
async def capture_and_send_video(websocket):
    # 初始化视频捕获设备，使用默认摄像头（参数0表示默认摄像头）
    cap = cv2.VideoCapture(0)
    # 设置视频捕获的分辨率，宽度为400像素，高度为300像素
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    # 进入无限循环，持续捕获视频帧并发送到WebSocket服务器
    while True:
        # 逐帧捕获视频
        ret, frame = cap.read()
        if not ret:
            # 如果无法接收帧（流结束），则退出循环
            print("Can't receive frame (stream end?). Exiting ...")
            break
            # 将BGR格式的帧转换为RGB格式
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 将帧转换为PIL图像对象
        pil_image = Image.fromarray(frame)
        # 创建一个BytesIO对象作为缓冲区，用于存储图像数据
        buffered = BytesIO()
        # 将PIL图像保存到缓冲区中，格式为JPEG
        pil_image.save(buffered, format="JPEG")
        # 对缓冲区中的图像数据进行base64编码，并将编码结果转换为字符串格式
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        # 构造一个数据URI，格式为'data:image/jpeg;base64,{img_base64}'，用于在WebSocket中发送图像数据
        img_data_uri = f'data:image/jpeg;base64,{img_base64}'
        # 向WebSocket服务器发送一个字符串"你好"（这里可能是为了测试服务器是否正常工作）
        await websocket.send("你好")
        # 向WebSocket服务器发送图像数据URI，包含捕获的实时视频帧
        await websocket.send(img_data_uri)
        # 等待0.043秒（这里的时间间隔可能需要根据实际需要进行调整）
        await asyncio.sleep(0.043)

    # 定义一个异步函数，作为主函数运行，建立WebSocket连接并启动视频捕获和发送过程


async def main():
    # 使用websockets库的connect方法建立WebSocket连接，连接到指定的WebSocket服务器地址和端口号
    async with websockets.connect(WEBSOCKET_URI) as websocket:
        # 调用capture_and_send_video函数，开始捕获视频并发送到WebSocket服务器
        await capture_and_send_video(websocket)

    # 使用asyncio库的run方法运行main函数，启动整个异步程序（包括WebSocket连接和视频捕获发送过程）


asyncio.run(main())