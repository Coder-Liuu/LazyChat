from textual.reactive import reactive
from textual.widgets import Static


class NewLabel(Static):
    DEFAULT_CSS = """
   NewLabel{
        content-align-horizontal: center;
        content-align-vertical: middle;
        width: 100%;
        color: white;
    } 
    """
    text = reactive("ChatAll")

    def render(self) -> str:
        return f"{self.text}"
