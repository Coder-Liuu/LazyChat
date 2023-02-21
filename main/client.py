import selectors
import struct
import json
import socket
import threading
import time

from Message import LoginRequestMessage, Message, ChatAllRequestMessage


def send_msg(sock, req):
    # 序列化成json字符串，再编码成utf-8格式的bytes
    data = json.dumps(req.to_dict()).encode('utf-8')

    # 打包数据
    magic_num = 0x01020304  # 魔数
    version = 1  # 版本号
    serializer_type = 0  # 序列化类型，0表示JSON
    msg_type = req.message_type  # 消息类型，1表示登录请求
    padding = 0xff  # 填充字节，没有实际用处
    data_len = len(data)  # 数据部分的长度

    # 使用struct模块进行打包，按照 ">i B B B B i" 的格式打包
    packed_data = struct.pack('>i B B B B i', magic_num, version, serializer_type, msg_type, padding, data_len)
    # 将数据部分拼接到打包好的数据中
    packed_data += data
    sock.sendall(packed_data)  # 发送数据
    print("read", req)


def recv_msg(sock):
    # 接收服务器返回的数据
    received_bytes = sock.recv(1024)

    # 解包收到的数据
    magic_num, version, serializer_type, msg_type, padding, data_len = \
        struct.unpack('>i B B B B i', received_bytes[:12])
    # 将数据部分提取出来
    data = received_bytes[12:12 + data_len]
    # 将收到的数据解码为utf-8编码的字符串，再反序列化为字典对象
    data = json.loads(data.decode())
    # 根据消息类型创建相应的消息对象，并从字典中还原消息的属性
    msg = Message.get_message_class(message_type=msg_type)
    resp = msg.from_dict(data)
    print("resp: ", resp)
    return resp


# 发送数据给Netty服务端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))  # 连接服务器


username = input("input username: ")
password = "123"

# 创建一个登录请求对象
msg = LoginRequestMessage(username, password)
send_msg(client, msg)
resp = recv_msg(client)

client.setblocking(False)
sel = selectors.DefaultSelector()
sel.register(client, selectors.EVENT_READ, recv_msg)

# 发送全局消息
# msg = ChatAllRequestMessage("hello", "zhangsan")
# send_msg(client, msg)

# msg = ChatAllRequestMessage("hi", "zhangsan")
# send_msg(client, msg)

class ReadThread(threading.Thread):
    def run(self) -> None:
        while True:
            events = sel.select()  # 默认是阻塞，有活动连接就返回活动的连接列表
            # 这里看起来是select，其实有可能会使用epoll，如果你的系统支持epoll，那么默认就是epoll
            for key, _ in events:
                callback = key.data  # 注册的回调函数
                callback(key.fileobj)  #


readThread = ReadThread()
readThread.start()

while True:
    content = input("msg: ")
    msg = ChatAllRequestMessage(content, username)
    send_msg(client, msg)


client.close()
