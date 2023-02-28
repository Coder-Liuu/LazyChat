import os
import random
import selectors
import struct
import json
import socket
import threading
from multiprocessing import Process, Queue

from Message import LoginRequestMessage, Message, ChatAllRequestMessage

queue = Queue()


class Conn:
    def __init__(self, queue):
        # 发送数据给Netty服务端
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('localhost', 8080))  # 连接服务器
        self.username = random.choice(["zhangsan", "lisi", "wangwu"])
        self.queue = queue

    def login(self):
        password = "123"
        # 创建一个登录请求对象
        msg = LoginRequestMessage(self.username, password)
        self.send_msg(msg)
        return self.recv_msg()

    def send_msg(self, req):
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
        self.conn.sendall(packed_data)  # 发送数据
        print("read", req)

    def recv_msg(self) -> Message:
        # 接收服务器返回的数据
        received_bytes = self.conn.recv(12)

        # 解包收到的数据
        magic_num, version, serializer_type, msg_type, padding, data_len = \
            struct.unpack('>i B B B B i', received_bytes[:12])

        # 将数据部分提取出来
        data = self.conn.recv(data_len)
        # 将收到的数据解码为utf-8编码的字符串，再反序列化为字典对象
        data = json.loads(data.decode())
        # 根据消息类型创建相应的消息对象，并从字典中还原消息的属性
        msg = Message.get_message_class(message_type=msg_type)
        resp = msg.from_dict(data)
        print("resp: ", resp)
        return resp

    def run(self):
        # 开始监听消息
        self.conn.setblocking(False)
        sub_p = Process(target=self.listen_recv, name="监听线程", args=(self.queue,))
        sub_p.daemon = True
        sub_p.start()

        # 监听消息队列
        queue_p = Process(target=self.listen_queue, name="消息队列", args=(self.queue,))
        queue_p.daemon = True
        queue_p.start()

        # 接受输入消息
        self.input()

    def listen_recv(self, queue):
        sel = selectors.DefaultSelector()
        sel.register(self.conn, selectors.EVENT_READ, self.recv_msg)

        while True:
            event = sel.select()
            for key, _ in event:
                callback = key.data
                resp = callback()
                queue.put(resp)
                print("队列 put:", resp, os.getpid())

    def listen_queue(self, queue):
        print("消息队列启动")
        while True:
            resp = queue.get()
            print("队列 get:", resp)

    def input(self):
        while True:
            data = input("你想说:")
            data = ChatAllRequestMessage(data, self.username)
            self.send_msg(data)


if __name__ == "__main__":
    print("begin", os.getpid())
    client = Conn(queue)
    client.login()
    client.run()
    print("over", os.getpid())
