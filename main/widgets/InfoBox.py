import logging

from textual.app import ComposeResult
from textual.widgets import Static, Label

from main.widgets.tools.NewLabel import NewLabel

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
        yield Label("\n查询帮助请按h")
        yield Label("执行命令请按c")
        yield Label("查看通知请按m")
