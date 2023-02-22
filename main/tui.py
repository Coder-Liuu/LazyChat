from textual.app import App, ComposeResult, CSSPathType, AutopilotCallbackType, ReturnType
from textual.widgets import Static, TextLog, Input, ListView, ListItem, Label


class Content(Static):
    CSS_PATH = "ui/tui.css"

    def __init__(self, classes):
        super().__init__(classes=classes)
        self.list = ListView(
            ListItem(Label("  "), classes="blank")
        )

    def compose(self) -> ComposeResult:
        yield Label("Content", classes="center_label")
        yield self.list

    def append(self, value):
        self.list.append(ListItem(Label(value), classes="blank"))


class TermApp(App):
    CSS_PATH = "ui/tui.css"

    def __init__(self):
        super().__init__()
        self.input = Input(placeholder="Enter your name")
        self.hello = Content(classes="content_box")
        self.content = ""

    def compose(self) -> ComposeResult:
        yield self.hello
        yield self.input

    def on_input_changed(self, event: Input.Changed) -> None:
        print(event)

    def on_input_submitted(self, event: Input.Submitted):
        self.hello.append(event.value)
        self.input.value = ""
        print("submit ok", event.value)


if __name__ == "__main__":
    app = TermApp()
    app.run()
