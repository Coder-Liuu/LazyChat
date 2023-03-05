from textual.app import ComposeResult, App
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static
from rich.markdown import Markdown

WELCOME_MD = """\
# Welcome LazyChat!

LazyChat是基于*Textual*一款终端聊天应用程序

## Dune quote

> "I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."

"""


class Welcome(Screen):
    DEFAULT_CSS = """
        Welcome {
            width: 100%;
            height: 100%;
            background: $surface;
        }

        Welcome Container {
            padding: 1;
            background: $panel;
            color: $text;
        }

        Welcome #text {
            margin:  0 1;
        }
    """
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Container(Static(Markdown(WELCOME_MD), id="text"), id="md")


if __name__ == '__main__':
    class WelcomeApp(App):
        def compose(self) -> ComposeResult:
            yield Welcome()

        def on_button_pressed(self) -> None:
            self.exit()


    app = WelcomeApp()
    app.run()
