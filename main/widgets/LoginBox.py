import logging

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input

from message import LoginRequestMessage

from widgets.Tip import Tip

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class LoginBox(Screen):
    DEFAULT_CSS = """
    LoginBox {
        align: center middle;
    }

    LoginBox>Static {
        align: center middle;
    }

    #title {
        content-align-horizontal: center;
        text-style: reverse;
    }
    """
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_mount(self) -> None:
        self.username = "zhangsan"
        self.password = "12"

        self.tip = Tip()
        self.app.install_screen(self.tip, name="tip")
        # 聚焦到下一个部件
        self.focus_next()

    def compose(self) -> ComposeResult:
        yield Static("欢迎登陆[b]TermAPP[/b]", id="title")
        yield Input(placeholder="账号", name="username")
        yield Input(placeholder="密码", password=True, name="password")

    def on_input_changed(self, event: Input.Changed):
        if event.input.name == "username":
            self.username = event.value
        elif event.input.name == "password":
            self.password = event.value

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.name in ["username", "password"]:
            req = LoginRequestMessage(self.username, self.password)
            self.app.core.send_msg(req)
            resp = self.app.core.recv_msg()
            if resp.success:
                self.app.username = self.username
                self.app.pop_screen()
                self.app.core_run()
            else:
                self.tip.update(resp.msg + "\n" + "按回车键重新登陆")
                self.app.push_screen('tip')


if __name__ == "__main__":
    class BSODApp(App):
        SCREENS = {"bsod": LoginBox()}
        BINDINGS = [("b", "push_screen('bsod')", "BSOD")]


    app = BSODApp()
    app.run()
