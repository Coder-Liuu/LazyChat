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
        yield Label("切换焦点TAB  查询帮助?")
        yield Label("执行命令/    查看通知m")
