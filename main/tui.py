import os
import threading
import random
from multiprocessing import Process

from textual.app import App, ComposeResult, CSSPathType, AutopilotCallbackType, ReturnType
from textual.widgets import Static, TextLog, Input, ListView, ListItem, Label
from Message import ChatAllRequestMessage, LoginRequestMessage


class Content(Static):
    CSS_PATH = "ui/tui.css"

    def __init__(self, classes):
        super().__init__(classes=classes)
        self.list = ListView(
            ListItem(Label("  "), classes="blank")
        )

    def compose(self) -> ComposeResult:
        yield Label("Content", classes="center_label")
        yield self.list

    def append(self, value):
        self.list.append(ListItem(Label(value), classes="blank"))


class TermApp(App):
    CSS_PATH = "ui/tui.css"

    def __init__(self, core):
        super().__init__()
        self.username = random.choice(["zhangsan", "lisi", "wangwu"])
        self.core = core

        self.input = Input(placeholder="Enter your name")
        self.content = Content(classes="content_box")

    def login(self):
        password = "123"
        # 创建一个登录请求对象
        msg = LoginRequestMessage(self.username, password)
        self.core.send_msg(msg)
        self.core.recv_msg()
        self.core.run()
        return True

    def compose(self) -> ComposeResult:
        yield self.content
        yield self.input

    def on_input_submitted(self, event: Input.Submitted):
        print("on_input_submitted")
        msg = ChatAllRequestMessage(event.value + "\n", self.username)
        self.core.send_msg(msg)
        self.content.append("my: " + event.value)
        self.input = ""

    def runAll(self):
        print(type(self.core.queue))
        queue_p = Process(target=self.listen_queue, name="消息队列", args=(self.core.queue,))
        queue_p.daemon = True
        queue_p.start()
        self.run()


    def listen_queue(self, queue):
        print("消息队列启动")
        while True:
            resp = queue.get()
            # self.content.append("server: " + resp.content)
            print("队列 get:", resp, os.getpid())


if __name__ == "__main__":
    from corenet import queue
    from corenet import CoreNet

    core = CoreNet(queue)
    app = TermApp(core)
    app.login()
    app.runAll()
