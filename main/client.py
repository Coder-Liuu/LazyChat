import struct
import json
import socket
from Message import LoginRequestMessage, Message



def send_msg(sock, req):
    # 序列化成json字符串，再编码成utf-8格式的bytes
    data = json.dumps(req.to_dict()).encode('utf-8')

    # 打包数据
    magic_num = 0x01020304  # 魔数
    version = 1  # 版本号
    serializer_type = 0  # 序列化类型，0表示JSON
    msg_type = 1  # 消息类型，1表示登录请求
    padding = 0xff  # 填充字节，没有实际用处
    data_len = len(data)  # 数据部分的长度

    # 使用struct模块进行打包，按照 ">i B B B B i" 的格式打包
    packed_data = struct.pack('>i B B B B i', magic_num, version, serializer_type, msg_type, padding, data_len)
    # 将数据部分拼接到打包好的数据中
    packed_data += data
    sock.sendall(packed_data)  # 发送数据


def recv_msg(sock):
    # 接收服务器返回的数据
    received_bytes = sock.recv(1024)

    # 解包收到的数据
    magic_num, version, serializer_type, msg_type, padding, data_len = \
        struct.unpack('>i B B B B i', received_bytes[:12])
    # 将数据部分提取出来
    data = received_bytes[12:]
    # 将收到的数据解码为utf-8编码的字符串，再反序列化为字典对象
    data = json.loads(data.decode())
    # 根据消息类型创建相应的消息对象，并从字典中还原消息的属性
    msg = Message.get_message_class(message_type=msg_type)
    resp = msg.from_dict(data)
    return resp


# 发送数据给Netty服务端
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))  # 连接服务器

# 创建一个登录请求对象
msg = LoginRequestMessage('zhangsan', '123')
send_msg(sock, msg)
resp = recv_msg(sock)
print(resp)
