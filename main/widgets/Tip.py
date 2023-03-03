from textual.app import RenderResult
from textual.screen import Screen


class Tip(Screen):
    BINDINGS = [("enter", "app.pop_screen", "Pop screen")]

    def update(self, text):
        self.text = text

    def render(self) -> RenderResult:
        return self.text
