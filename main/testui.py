import os
import random
from multiprocessing import Process

from main.Message import ChatAllRequestMessage, LoginRequestMessage
from main.corenet import CoreNet, queue


def listen_queue(queue):
    while True:
        resp = queue.get()
        print("队列 get:", resp, os.getpid())


class TestUI:
    def __init__(self, coreNet):
        self.username = random.choice(["zhangsan", "lisi", "wangwu"])
        self.core = coreNet

    def login(self):
        password = "123"
        # 创建一个登录请求对象
        msg = LoginRequestMessage(self.username, password)
        self.core.send_msg(msg)
        self.core.recv_msg()
        self.core.run()
        return True

    def run(self):
        # 监听消息队列
        queue_p = Process(target=listen_queue, name="消息队列", args=(self.core.queue,))
        queue_p.daemon = True
        queue_p.start()

        while True:
            data = input("你想说:")
            data = ChatAllRequestMessage(data, self.username)
            self.core.send_msg(data)


if __name__ == "__main__":
    print("begin", os.getpid())
    coreNet = CoreNet(queue)
    ui = TestUI(coreNet)
    ui.login()
    ui.run()
    print("over", os.getpid())
