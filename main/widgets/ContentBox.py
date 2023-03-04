import logging

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Static, ListView, ListItem, Label

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class NewLabel(Static):
    text = reactive("ChatAll")

    def render(self) -> str:
        return f"{self.text}"


class ContentBox(Static):
    DEFAULT_CSS = """
    .content_box {
        height: 3fr;
        border: solid green;
    }

    """

    def __init__(self, classes):
        super().__init__(classes=classes)
        self.label = NewLabel(classes="center_label")
        self.list = ListView()
        self.map = dict()

    def compose(self) -> ComposeResult:
        yield self.label
        yield self.list

    def update_list(self, name):
        self.list.clear()
        if not self.map.get(name) is None:
            for item in self.map.get(name).split("\n"):
                item = self.__warp_item(item)
                self.list.append(item)

    def __warp_item(self, value):
        label = Label(value.strip())
        container = Container(label, classes="blank")
        return ListItem(container)

    def append(self, value):
        if self.map.get(self.label.text) is None:
            self.map[self.label.text] = ""

        self.map[self.label.text] += value
        self.list.append(self.__warp_item(value))
        logging.debug(f"append {self.label.text} {self.map[self.label.text]}")
