import logging

from textual.app import ComposeResult
from textual.widgets import Static, Label

from LazyChat.widgets.tools.NewLabel import NewLabel

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class InfoBox(Static):
    DEFAULT_CSS = """
    InfoBox {
        width: 100%;
        height: 18%;
        border: solid green;
    }
    """
    title = NewLabel()

    def compose(self) -> ComposeResult:
        yield self.title
        yield Label("按键说明")
        yield Label("切换焦点TAB")
        yield Label("查询帮助h  执行命令c")
        yield Label("查看通知m")
