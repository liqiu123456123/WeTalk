# 导入所需的库
import asyncio
import websockets
import pyaudio

# 定义音频块的大小，这里是4096字节
chunk = 4096

# 定义音频样本的格式为16位整数
sample_format = pyaudio.paInt16

# 定义声道数为2，即立体声
channels = 2

# 定义采样率为44100Hz
fs = 44100

# 创建一个PyAudio实例，用于音频输入和输出
p = pyaudio.PyAudio()

# 打开麦克风输入流
micstream = p.open(format=sample_format,
                   channels=channels,
                   rate=fs,
                   frames_per_buffer=chunk,
                   input=True)

# 打开音频输出流
stream2 = p.open(format=sample_format,
                 channels=channels,
                 rate=fs,
                 frames_per_buffer=chunk,
                 output=True)


# 定义一个异步函数echo，用于处理WebSocket连接
async def echo(websocket, path):
    # 打印websockets.serve的信息（但实际上这里应该是websockets.serve()的调用信息）
    print(websockets.serve)

    # 异步迭代WebSocket接收到的消息
    async for message in websocket:
        # 将接收到的WebSocket消息写入音频输出流（播放音频）
        print(message)
        stream2.write(message)  # 播放

        # 初始化一个空列表y，用于存储从麦克风读取的音频数据
        y = []

        # 从麦克风读取一块音频数据（这里只读取一次）
        for i in range(1):
            m = micstream.read(chunk)
            y.append(m)

            # 如果WebSocket消息的长度大于1，则将其（以及从麦克风读取的数据）发送回WebSocket客户端
        if len(message) > 1: await websocket.send(y)

    # 定义一个异步函数main，用于启动WebSocket服务器


async def main():
    # 使用websockets库启动WebSocket服务器，监听指定IP和端口，并处理连接使用echo函数
    async with websockets.serve(echo, "192.168.60.105", 8765):
        # 创建一个未完成的Future对象，使得服务器持续运行，直到被外部因素（如Ctrl+C）中断
        await asyncio.Future()  # run forever


# 使用asyncio库运行main函数，启动WebSocket服务器
asyncio.run(main())