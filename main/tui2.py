import logging
import os
import random
from queue import Queue

from textual.app import App, ComposeResult
from textual.widgets import Static, Input, ListView, ListItem, Label
from Message import ChatAllRequestMessage, LoginRequestMessage
from corenet import CoreNet
import asyncio


logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')



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

    @classmethod
    def run(cls, core):
        async def run_app():
            app = cls(core)
            await app._process_messages()
        asyncio.run(run_app())

    def compose(self) -> ComposeResult:
        yield self.content
        yield self.input

    def on_load(self):
        self.username = random.choice(["zhangsan", "lisi", "wangwu"])
        msg = LoginRequestMessage(self.username, "123")
        self.core.send_msg(msg)
        self.core.recv_msg()
        self.core.run()

        logging.debug("on load")

        s = "PID: " + str(os.getpid())
        self.input = Input(placeholder="Enter your name" + s)
        self.content = Content(classes="content_box")
        self.set_interval(0.3, self.server_listen)


    def server_listen(self):
        logging.debug("server_listen")
        logging.debug(self.core.queue.qsize())
        if self.core.queue.qsize():
            message = self.core.queue.get()
            self.content.append(message.content)

            # logging.debug("queue get",message)


    def on_input_submitted(self, event: Input.Submitted):
        logging.debug("on_input_submitted")
        msg = ChatAllRequestMessage(event.value + "\n", self.username)

        logging.debug("send_msg")
        self.core.send_msg(msg)
        self.content.append("my: " + event.value)
        self.input.value = ""
        logging.debug(self.core.queue)



if __name__ == "__main__":
    queue = Queue()
    core = CoreNet(queue)
    TermApp.run(core)
    # app = TermApp(core)
    # app.login()
    # app.runAll()
