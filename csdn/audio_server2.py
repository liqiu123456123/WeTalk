# 复制粘贴即可，细节自己百度，主要是跑通程序
import base64
import asyncio
import websockets
import cv2
import math
import np
import pyaudio
import wave
import time
import threading
import matplotlib.pyplot as plt

chunk = 4096  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2  # 两声道
fs = 44100  # Record at 44100 samples per second
p = pyaudio.PyAudio()  # 创建音频对象

# image = cv2.imread("1.png")#image :是返回提取到的图片的值
# 麦克风
micstream = p.open(format=sample_format,  # 音频输入流创建
                   channels=channels,
                   rate=fs,
                   frames_per_buffer=chunk,
                   input=True)
# 喇叭
stream2 = p.open(format=sample_format,  # 音频输出流创建
                 channels=channels,
                 rate=fs,
                 frames_per_buffer=chunk,
                 output=True)


async def echo(websocket, path):
    print(websockets.serve)
    async for message in websocket:
        stream2.write(message)  # 播放
        # m=micstream.read(chunk)#录音
        y = []
        for i in range(1):  # 这里和上一篇数字不一样请注意。15次录音会阻塞线程。需要开新线程处理。范例用1次可忽略阻塞影响。
            m = micstream.read(chunk)
            y.append(m)

        if len(message) > 1: await websocket.send(y)  # 发送录音


async def main():
    # start a websocket server
    async with websockets.serve(echo, "192.168.60.105", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
