import json
import logging
import os
import selectors
import socket
import struct
import threading

from LazyChat.message import Message

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')



class CoreNet:
    def __init__(self, queue, IP_ADDR, PORT):
        # 发送数据给Netty服务端
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器
        self.conn.connect((IP_ADDR, PORT))
        # 消息队列
        self.queue = queue

    def __del__(self):
        self.conn.close()

    def send_msg(self, req):
        logging.debug(f"coreNet sendMsg: {req}")
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
        logging.debug(f"send_msg: {packed_data}")

    def recv_msg(self) -> Message:
        # 接收服务器返回的数据
        received_bytes = self.conn.recv(12)
        logging.debug(f"received_bytes {received_bytes}")

        # 解包收到的数据
        magic_num, version, serializer_type, msg_type, padding, data_len = \
            struct.unpack('>i B B B B i', received_bytes[:12])

        # 将数据部分提取出来
        data = self.conn.recv(data_len)
        logging.debug(f"data {data}")
        # 将收到的数据解码为utf-8编码的字符串，再反序列化为字典对象
        data = json.loads(data.decode())
        # 根据消息类型创建相应的消息对象，并从字典中还原消息的属性
        msg = Message.get_message_class(message_type=msg_type)
        resp = msg.from_dict(data)
        logging.debug("recv_msg: {}".format(resp))
        return resp

    def run(self):
        logging.debug("开始监听消息")
        self.conn.setblocking(False)
        t1 = threading.Thread(target=self.listen_recv, name="消息队列", args=(self.queue,))
        t1.setDaemon(True)
        t1.start()

    def listen_recv(self, queue):
        sel = selectors.DefaultSelector()
        sel.register(self.conn, selectors.EVENT_READ, self.recv_msg)

        while True:
            event = sel.select()
            for key, _ in event:
                callback = key.data
                resp = callback()
                queue.put(resp)
                logging.debug(f"queue put: {resp} {os.getpid()}")
