import logging

from textual.app import RenderResult, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Input

from LazyChat.message import NoticeRequestMessage

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class CommandBox(Widget):
    DEFAULT_CSS = """
    CommandBox {
        layer: above;
        width: 35%;
        height: 25%;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
    }
    """
    inputBox = Input(placeholder="例如: /add 好友名字", name="command")

    def compose(self) -> ComposeResult:
        yield Label("执行命令\n",classes="center_label")
        yield self.inputBox

    def on_input_submitted(self, event: Input.Submitted):
        _input = event.value
        if event.input.name == "command":
            index = _input.find(' ')
            notice = _input[:index]
            value = _input[index + 1:]
            if notice == "/add":
                msg = NoticeRequestMessage(1, self.app.username, value)
                self.app.core.send_msg(msg)
            self.inputBox.value = ""

            # logging.debug(f"command: {}-----{_input[index + 1:]}")
            # self.app._action_remove_commandBox()
            # self.styles.display = "none"
