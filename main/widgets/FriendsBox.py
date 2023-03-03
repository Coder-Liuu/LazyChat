import logging

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, ListView, ListItem, Label

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class FriendsBox(Static):
    def __init__(self, classes):
        super().__init__(classes=classes)

        self.list = ListView(
            ListItem(Label("ChatAll"), name="ChatAll"),
            ListItem(Label("lisi"), name="lisi"),
        )

    def compose(self) -> ComposeResult:
        yield Label("Friends", classes="center_label")
        yield self.list

    def append(self, value):
        label = Label(value)
        container = Container(label, classes="blank")
        item = ListItem(container)
        self.list.append(item)

    def on_list_view_selected(self, item: ListView.Selected):
        name = item.item.name
        self.app.contentBox.label.text = name
        self.app.contentBox.update_list(name)
        logging.debug(f"on_list_view_selected: ok {item.item.name}")
