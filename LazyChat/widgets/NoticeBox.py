import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Label, ListView, ListItem

from LazyChat.message import NoticeRequestMessage, MessageTypes

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class NoticeBox(Widget):
    BINDINGS = [
        Binding("l", "select_cursor", "Select", show=False),
        Binding("h", "remove_cursor", "Select", show=False),
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
    ]

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
    noticeList = ListView()

    def compose(self) -> ComposeResult:
        yield Label("消息通知:bulb:", classes="center_label")
        yield self.noticeList

    def append(self, value, name):
        item = ListItem(Label(value), name=name)
        self.noticeList.append(item)

    def action_select_cursor(self):
        self.noticeList.action_select_cursor()

        highlighted = self.noticeList.highlighted_child
        name = highlighted.name
        highlighted.remove()
        self.noticeList.action_cursor_up()

        # 发送都同意的请求
        msg = NoticeRequestMessage(MessageTypes.NOTICE_FRIEND_AGREE, name, self.app.username)
        self.app.core.send_msg(msg)

    def action_remove_cursor(self):
        self.noticeList.action_select_cursor()

        highlighted = self.noticeList.highlighted_child
        name = highlighted.name
        highlighted.remove()
        self.noticeList.action_cursor_up()
        # 发送拒绝的请求
        msg = NoticeRequestMessage(MessageTypes.NOTICE_FRIEND_REFUSE, name, self.app.username)
        self.app.core.send_msg(msg)

    def action_cursor_up(self):
        self.noticeList.action_cursor_up()

    def action_cursor_down(self):
        self.noticeList.action_cursor_down()
