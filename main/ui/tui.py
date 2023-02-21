from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.geometry import Size
from textual.widget import Widget
from textual.widgets import Header, Button, Static
from textual_extras.widgets import List



class TermChat(App):

    # 键位绑定
    BINDINGS = [
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield List()


if __name__ == "__main__":
    app = TermChat()
    app.run()
