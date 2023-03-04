import logging

from textual.app import RenderResult, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Input, ListView, ListItem

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class NoticeBox(Widget):
    DEFAULT_CSS = """
    NoticeBox {
        layer: above;
        width: 35%;
        height: 25%;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
    }
    """
    noticeList = ListView(
        ListItem(Label("张三想添加你为好友")),
    )

    def compose(self) -> ComposeResult:
        yield Label("消息通知\n",classes="center_label")
        yield self.noticeList
