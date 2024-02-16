import base64
import asyncio
import websockets
import cv2
import math
import np


async def echo(websocket, path):
    # fetch msg
    async for message in websocket:
        # 检查连接状态并输出提示信息
        print(message)
        if message == '你好':
            pass
        else:
            imm = base64.b64decode(message.split(',')[1])  # 去掉类型头
            im = np.asarray(list(imm), dtype="uint8")  # 解码成cv2可阅读的格式
            im2 = cv2.imdecode(im, cv2.IMREAD_COLOR)
            cv2.imshow('Image111111', im2)
            cv2.waitKey(1)

async def main():
    #
    async with websockets.serve(echo, "192.168.60.105", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())

