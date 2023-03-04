import logging

from textual.app import RenderResult, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Input

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
        if event.input.name == "command":
            logging.debug(f"command: {event.value}")
            self.app.action_remove_commandBox()
            # self.styles.display = "none"
