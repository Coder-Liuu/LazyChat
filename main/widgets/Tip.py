from textual.app import RenderResult
from textual.screen import Screen


class Tip(Screen):
    DEFAULT_CSS = """
    Tip {
        width: 50%;
        height: 50%;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
        align: center middle;
        content-align: center middle;
    }
    """
    BINDINGS = [("enter", "app.pop_screen", "Pop screen")]

    def update(self, text):
        self.text = text

    def render(self) -> RenderResult:
        return self.text
