import selectors
import struct
import json
import socket
import threading

from Message import LoginRequestMessage, Message


class Conn:
    def __init__(self, tui):
        # 发送数据给Netty服务端
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('localhost', 8080))  # 连接服务器
        self.username = "zhangsan"
        self.tui = tui

    def login(self):
        password = "123"
        # 创建一个登录请求对象
        msg = LoginRequestMessage(self.username, password)
        self.send_msg(msg)
        return self.recv_msg()

    def run(self):
        # 开始监听消息
        self.conn.setblocking(False)
        sel = selectors.DefaultSelector()
        sel.register(self.conn, selectors.EVENT_READ, self.recv_msg)
        self.listen_msg(sel)

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

    def listen_msg(self, sel):
        class ReadThread(threading.Thread):
            def __init__(self, tui):
                super().__init__()
                self.tui = tui
                print("tui", id(self.tui))

            def run(self) -> None:
                print("sub thread run")
                while True:
                    print(sel)
                    print("sub thread event")
                    r = sel.select()  # 默认是阻塞，有活动连接就返回活动的连接列表

                    # 这里看起来是select，其实有可能会使用epoll，如果你的系统支持epoll，那么默认就是epoll
                    for key, mark in r:
                        print(r)
                        callback = key.data  # 注册的回调函数
                        resp = callback()

        self.readThread = ReadThread(self.tui)
        # 关闭守护进程模式
        print("readThread create")
        self.readThread.setDaemon(True)
        self.readThread.start()


if __name__ == "__main__":
    client = Conn(None)
    client.login()
    client.run()
