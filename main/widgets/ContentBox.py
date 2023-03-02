from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, ListView, ListItem, Label


class ContentBox(Static):
    def __init__(self, classes):
        super().__init__(classes=classes)
        self.list = ListView(
            # ListItem(Label("  "), classes="blank")
        )

    def compose(self) -> ComposeResult:
        yield Label("Content", classes="center_label")
        yield self.list

    def append(self, value):
        label = Label(value[:-1])
        container = Container(label, classes="blank")
        item = ListItem(container)
        self.list.append(item)
