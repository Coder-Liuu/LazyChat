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
        # 为了不紧凑，所以加\n
        yield Label("执行命令:blue_car: \n", classes="center_label")
        yield self.inputBox

    def on_input_submitted(self, event: Input.Submitted):
        _input = event.value
        if event.input.name != "command":
            return

        index = _input.find(' ')
        notice = _input[:index]
        value = _input[index + 1:]
        if notice == "/add":
            value = value.strip()
            if value == self.app.username:
                self.app.on_tip_box("不能添加自己为好友")
                return

            msg = NoticeRequestMessage(1, self.app.username, value)
            self.app.core.send_msg(msg)
        self.inputBox.value = ""
