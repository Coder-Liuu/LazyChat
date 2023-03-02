import logging
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input

from Message import LoginRequestMessage, LoginResponseMessage

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class LoginBox(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_load(self):
        self.username = ""
        self.password = ""

    def compose(self) -> ComposeResult:
        yield Static("欢迎登陆TermAPP", id="title")
        yield Input(placeholder="账号", name="username")
        yield Input(placeholder="密码", password=True, name="password")

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.name == "username":
            self.username = event.value
        elif event.input.name == "password":
            self.password = event.value

            req = LoginRequestMessage(self.username, self.password)
            self.app.core.send_msg(req)
            resp = self.app.core.recv_msg()
            if resp.success:
                self.app.pop_screen()
            else:
                pass

            logging.debug(f"recv msg: {resp}")


if __name__ == "__main__":
    class BSODApp(App):
        SCREENS = {"bsod": LoginBox()}
        BINDINGS = [("b", "push_screen('bsod')", "BSOD")]
    app = BSODApp()
    app.run()
