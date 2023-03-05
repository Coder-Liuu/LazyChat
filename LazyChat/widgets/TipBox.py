import logging

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Label

from LazyChat.widgets.tools.NewLabel import NewLabel

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class TipBox(Widget):
    DEFAULT_CSS = """
    TipBox {
        layer: above;
        width: 35%;
        height: 25%;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
    }
    """
    content = NewLabel()

    def compose(self) -> ComposeResult:
        yield Label("提示框\n", classes="center_label")
        yield self.content
