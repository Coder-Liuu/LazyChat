import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Static, ListView, ListItem, Label

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class FriendsBox(Static):
    DEFAULT_CSS = """
    FriendsBox {
        width: 100%;
        height: 78%;
        border: solid green;
    }
    """
    BINDINGS = [
        Binding("l", "select_cursor", "Select", show=False),
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
    ]

    def __init__(self):
        super().__init__()

        self.list = ListView(
            ListItem(Label("ChatAll"), name="ChatAll"),
        )

    def action_select_cursor(self):
        self.list.action_select_cursor()
        logging.debug("action_focus_inputBox")
        self.app.action_focus_inputBox()

    def action_cursor_up(self):
        self.list.action_cursor_up()

    def action_cursor_down(self):
        self.list.action_cursor_down()

    def compose(self) -> ComposeResult:
        yield Label("Friends", classes="center_label")
        yield self.list

    def append(self, value, name):
        label = Label(value)
        container = Container(label, classes="blank")
        item = ListItem(container, name=name)
        self.list.append(item)

    def on_list_view_selected(self, item: ListView.Selected):
        name = item.item.name
        self.app.contentBox.label.text = name
        self.app.contentBox.update_list(name)
        logging.debug(f"on_list_view_selected: ok {item.item.name}")
