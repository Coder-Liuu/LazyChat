import logging
import random
from queue import Queue

from textual.app import App, ComposeResult
from textual.widgets import Input
from message import ChatAllRequestMessage
from corenet import CoreNet
from widgets.ContentBox import ContentBox
from widgets.LoginBox import LoginBox

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class TermApp(App):
    CSS_PATH = "ui/tui.css"
    BINDINGS = [("b", "push_screen('bsod')", "BSOD")]

    def __init__(self, core):
        super().__init__()
        self.username = random.choice(["zhangsan", "lisi", "wangwu"])
        self.core = core
        self.inputBox = Input(placeholder="Say Something", name="inputBox")
        self.contentBox = ContentBox(classes="content_box")

    @classmethod
    def runAll(cls, core):
        def run_app():
            app = cls(core)
            app.run()

        run_app()

    def compose(self) -> ComposeResult:
        yield self.contentBox
        yield self.inputBox

    def on_mount(self) -> None:
        self.install_screen(LoginBox(), name="bsod")
        self.push_screen('bsod')

    def core_run(self):
        self.set_interval(0.1, self.server_listen)
        self.core.run()

    def server_listen(self):
        if self.core.queue.qsize():
            message = self.core.queue.get()
            self.contentBox.append(message.content)

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.name == "inputBox":
            logging.debug("APP: on_input_submitted")

            msg = ChatAllRequestMessage(event.value + "\n", self.username)
            self.core.send_msg(msg)
            self.contentBox.append("my: " + event.value)
            self.inputBox.value = ""


if __name__ == "__main__":
    queue = Queue()
    core = CoreNet(queue)
    TermApp.runAll(core)
