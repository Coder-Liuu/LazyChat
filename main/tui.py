import logging
import random
from queue import Queue

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, Header

from widgets.FriendsBox import FriendsBox
from message import ChatAllRequestMessage, ChatToOneRequestMessage, ChatAllResponseMessage, ChatToOneResponseMessage
from corenet import CoreNet
from widgets.ContentBox import ContentBox
from widgets.LoginBox import LoginBox
from widgets.Welcome import Welcome

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class LazyChat(App):
    CSS_PATH = "ui/tui.css"
    BINDINGS = [("b", "push_screen('bsod')", "BSOD"),
                ("h", "push_screen('welcome')", "WelCome")
                ]

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.inputBox = Input(placeholder="Say Something", name="inputBox")
        self.contentBox = ContentBox(classes="content_box")
        self.header = Header(name="Welcome to TermApp", show_clock=True)
        self.friendsBox = FriendsBox(classes="horizontal")

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
            self.friendsBox,
            Vertical(
                self.contentBox,
                self.inputBox,
                classes="vertical"
            ),
        )

    def core_run(self):
        # 聚焦到下一个部件
        self.screen.focus_next()
        self.screen.focus_next()

        self.set_interval(0.1, self.server_listen)
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
