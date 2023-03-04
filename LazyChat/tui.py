import sys
import os

# 解决PyCharm的根路径的问题

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import logging
from queue import Queue

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Input, Header, Static, Label

from widgets.InfoBox import InfoBox
from widgets.CommandBox import CommandBox
from widgets.FriendsBox import FriendsBox
from message import ChatAllRequestMessage, ChatToOneRequestMessage, ChatAllResponseMessage, ChatToOneResponseMessage, \
    NoticeResponseMessage
from corenet import CoreNet
from widgets.ContentBox import ContentBox
from widgets.LoginBox import LoginBox
from widgets.Welcome import Welcome
from widgets.NoticeBox import NoticeBox

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class LazyChat(App):
    CSS_PATH = "ui/tui.css"
    BINDINGS = [
        ("b", "push_screen('bsod')", "BSOD"),
        ("h", "push_screen('welcome')", "WelCome"),
        ("c", "display_commandBox()", "DisPlay CommandBox"),
        ("m", "display_noticeBox()", "DisPlay NoticeBox"),
        ("escape ", "remove_box()", "Remove CommandBox"),
        ("ctrl+h", "focus_friendsBox()", "Focus FriendsBox"),
        ("q", "exit()", "Exit"),
        ("ctrl+q", "exit()", "Exit"),
    ]

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.inputBox = Input(placeholder=f"Say Something", name="inputBox")
        self.contentBox = ContentBox()
        self.header = Header(name="Welcome to TermApp", show_clock=True)
        self.friendsBox = FriendsBox()
        self.infoBox = InfoBox()

        self.commandBox = CommandBox(id="commandBox")
        self.commandBox.styles.display = "none"
        self.noticeBox = NoticeBox(id="noticeBox")
        self.noticeBox.styles.display = "none"

    def action_exit(self):
        exit(0)

    def action_display_noticeBox(self):
        self.set_focus(self.noticeBox.noticeList)
        self.noticeBox.styles.display = "block"

    def action_display_commandBox(self):
        self.set_focus(self.commandBox.inputBox)
        self.commandBox.styles.display = "block"

    def _action_remove_commandBox(self):
        self.set_focus(self.friendsBox.list)
        self.commandBox.styles.display = "none"

    def _action_remove_noticeBox(self):
        self.set_focus(self.friendsBox.list)
        self.noticeBox.styles.display = "none"

    def action_remove_box(self):
        if self.commandBox.styles.display == "block":
            self._action_remove_commandBox()
        elif self.noticeBox.styles.display == "block":
            self._action_remove_noticeBox()

    def action_focus_friendsBox(self):
        self.set_focus(self.friendsBox)

    def action_focus_inputBox(self):
        self.set_focus(self.inputBox)

    def on_mount(self) -> None:
        self.install_screen(LoginBox(), name="bsod")
        self.install_screen(Welcome(), name="welcome")
        self.push_screen('bsod')

    @classmethod
    def runAll(cls, core):
        def run_app():
            app = cls(core)
            app.run()

        run_app()

    def compose(self) -> ComposeResult:
        yield self.header
        yield Horizontal(
            Vertical(
                self.friendsBox,
                self.infoBox,
                classes="test_border"
            ),
            Vertical(
                self.contentBox,
                self.inputBox,
                classes="vertical"
            ),
        )
        yield self.commandBox
        yield self.noticeBox

    def core_run(self):
        # 聚焦到下一个部件
        self.set_focus(self.inputBox)
        self.set_interval(0.1, self.server_listen)
        self.infoBox.title.text = "当前用户\n" + self.username
        self.core.run()

    def server_listen(self):
        if self.core.queue.qsize():
            message = self.core.queue.get()
            logging.debug(f"server listen: {message} {type(message)}")
            if isinstance(message, ChatAllResponseMessage):
                if message.username == self.username:
                    self.contentBox.append(f"[bold red]{message.username}[/bold red] : {message.content}")
                else:
                    self.contentBox.append(f"[bold black]{message.username}[/bold black] : {message.content}")
            elif isinstance(message, ChatToOneResponseMessage):
                from_user = message.from_user
                if self.contentBox.map.get(from_user) is None:
                    self.contentBox.map[from_user] = ""
                self.contentBox.map[from_user] += f"[bold black]{message.from_user}[/bold black] : {message.content}"

                if from_user == self.contentBox.label.text:
                    self.contentBox.update_list(from_user)
            elif isinstance(message, NoticeResponseMessage):
                from_user = message.from_user
                to_user = message.to_user
                logging.debug(f"{message}")
                # 发起请求阶段
                if message.notice_type == 1:
                    self.noticeBox.append(f"[bold red]{from_user}[/bold red] 想添加你为好友", name=from_user)
                # 添加成功阶段
                elif message.notice_type == 2:
                    self.friendsBox.append(f"[bold red]{from_user}[/bold red]", name=from_user)


    def on_input_submitted(self, event: Input.Submitted):
        if event.input.name == "inputBox":
            to_user = self.contentBox.label.text
            if to_user == "ChatAll":
                logging.debug("APP: on_input_submitted")
                msg = ChatAllRequestMessage(event.value + "\n", self.username)
                self.core.send_msg(msg)
                self.inputBox.value = ""
            else:
                msg = ChatToOneRequestMessage(self.username, to_user, event.value + "\n")
                self.contentBox.append(f"[bold red]{self.username}[/bold red] : {event.value}\n")
                self.core.send_msg(msg)
                self.inputBox.value = ""


if __name__ == "__main__":
    queue = Queue()
    core = CoreNet(queue)
    LazyChat.runAll(core)
