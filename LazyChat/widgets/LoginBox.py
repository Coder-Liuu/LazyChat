import logging

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Input, Label

from LazyChat.message import LoginRequestMessage
from .tools.Tip import Tip

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class LoginBox(Screen):
    DEFAULT_CSS = """
    LoginBox {
        align: center middle;
    }

    LoginBox>Static {
        align: center middle;
    }
    LoginBox> Container{
        align: center middle;
        border: solid green;
    }

    #title {
        content-align-horizontal: center;
        text-style: reverse;
    }
    """
    BINDINGS = [("escape", "remove_tip", "Remove Tip Widget")]

    # 使用下面网站进行生成的：http://patorjk.com/software/taag/#p=testall&h=2&v=2&f=Univers&t=LAZYCHAT
    TITLE = """
      _                _______     _______ _    _       _______ 
     | |        /\    |___  | \   / / ____| |  | |   /\|__   __|
     | |       /  \      / / \ \_/ / |    | |__| |  /  \  | |   
     | |      / /\ \    / /   \   /| |    |  __  | / /\ \ | |   
     | |____ / ____ \  / /__   | | | |____| |  | |/ ____ \| |   
     |______/_/    \_\/_____|  |_|  \_____|_|  |_/_/    \_\_|   
    """

    tip = Tip()
    input_username = Input(placeholder="账号", name="username")
    input_password = Input(placeholder="密码", password=True, name="password")
    tip.styles.display = "none"

    def on_mount(self) -> None:
        self.username = "zhangsan"
        self.password = "123"

        # 聚焦到 input_username组件
        self.set_focus(self.input_username)

    def compose(self) -> ComposeResult:
        yield Container(Label(self.TITLE))
        yield self.input_username
        yield self.input_password
        yield self.tip

    def action_remove_tip(self):
        self.tip.styles.display = "none"

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
                self.tip.update(resp.msg + "\n" + "按[bold red][ESC][/bold red]关闭窗口 :vampire:")
                self.tip.styles.display = "block"


if __name__ == "__main__":
    class BSODApp(App):
        SCREENS = {"bsod": LoginBox()}
        BINDINGS = [("b", "push_screen('bsod')", "BSOD")]


    app = BSODApp()
    app.run()
