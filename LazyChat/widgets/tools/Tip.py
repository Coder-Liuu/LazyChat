from textual.app import RenderResult
from textual.widget import Widget
from textual.widgets import Static


class Tip(Widget):
    DEFAULT_CSS = """
    Tip {
        layer: above;
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
    text = ""

    def update(self, text):
        self.text = text

    def render(self) -> RenderResult:
        return self.text
