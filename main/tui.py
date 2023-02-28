from __future__ import annotations

import asyncio
import threading
from multiprocessing import Queue

from textual.app import App, ComposeResult, CSSPathType, AutopilotCallbackType, ReturnType
from textual.widgets import Static, TextLog, Input, ListView, ListItem, Label

from conn import Conn
from Message import ChatAllRequestMessage
from global_msg import queue_msg


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

    def __init__(self):
        super().__init__()
        self.input = Input(placeholder="Enter your name")
        self.content = Content(classes="content_box")
        self.sem = threading.Semaphore(0)
        self.get_recv = ""

        self.conn = Conn(self)
        self.conn.login()
        print("tui ----", id(self))



    # def run(self, *, headless: bool = False, size: tuple[int, int] | None = None,
    #         auto_pilot: AutopilotCallbackType | None = None) -> ReturnType | None:
    #     return super().run(headless=headless, size=size, auto_pilot=auto_pilot)

    def compose(self) -> ComposeResult:
        yield self.content
        yield self.input

    def on_input_submitted(self, event: Input.Submitted):
        print("on_input_submitted")
        msg = ChatAllRequestMessage(event.value + "\n", self.conn.username)
        self.conn.send_msg(msg)
        self.content.append("my: " + event.value)
        self.input.value = ""

        # self.sem.acquire()
        # print("get_recv", self.get_recv[0])
        # if len(content) > 0:

        # print("queue_msg", queue_msg.empty())
        # self.content.append("哈哈")
        if not queue_msg.empty():
            self.content.append(queue_msg.get())

    def gave_msg(self, content):
        print("gave_msg", content)
        self.get_recv = content


    def run(self, *, headless: bool = False, size: tuple[int, int] | None = None,
            auto_pilot: AutopilotCallbackType | None = None) -> ReturnType | None:
        super().run(headless=headless, size=size, auto_pilot=auto_pilot)
        return self.conn.run()

    def bind_client(self, client):
        self.conn = client


if __name__ == "__main__":
    app = TermApp()
    app.run()
    app.conn.run()
    # asyncio.run(main())
