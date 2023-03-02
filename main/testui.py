import os
import random
import threading
from queue import Queue
from threading import Thread

from Message import ChatAllRequestMessage, LoginRequestMessage
from corenet import CoreNet


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
        self.core.run(),
        return True

    def run(self):
        # 监听消息队列
        t1 = Thread(target=self.listen_queue, name="消息队列", args=(self.core.queue,))
        t1.setDaemon(True)
        t1.start()

        while True:
            data = input("你想说:")
            data = ChatAllRequestMessage(data, self.username)
            self.core.send_msg(data)

    def listen_queue(self, queue):
        while True:
            resp = queue.get()
            print("队列 get:", resp, threading.currentThread().getName())


if __name__ == "__main__":
    queue = Queue()
    coreNet = CoreNet(queue)
    ui = TestUI(coreNet)
    ui.login()
    ui.run()
