import sys
import os

# 解决PyCharm的根路径的问题

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import logging

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, Header

from LazyChat.utils.notification import notify_sound
from LazyChat.message import ChatAllRequestMessage, ChatToOneRequestMessage, ChatAllResponseMessage, ChatToOneResponseMessage, \
    NoticeResponseMessage, MessageTypes
from .widgets import InfoBox, CommandBox, FriendsBox, ContentBox, LoginBox, Welcome, NoticeBox, TipBox
from os import path

logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


class LazyChat(App):
    DEFAULT_CSS = """
        Screen {
            align: center middle;
            layers: basic above;
        }
        /* LazyChat */

        .test_border {
            /*border: solid green;*/
            width: 24%;
        }

        .vertical {
            width: 74%;
        }


        /* FriendsBox and ContentBox */
        .blank {
            align: left middle;
        }

        .center_label{
            content-align-horizontal: center;
            content-align-vertical: middle;
            width: 100%;
            color: white;
        }
    """
    BINDINGS = [
        ("?", "push_screen('welcome')", "WelCome"),
        ("/", "display_commandBox()", "DisPlay CommandBox"),
        ("m", "display_noticeBox()", "DisPlay NoticeBox"),
        ("escape ", "remove_box()", "Remove CommandBox"),
        ("q", "exit()", "Exit"),
        ("ctrl+q", "exit()", "Exit"),
    ]

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.inputBox = Input(placeholder=f"Say Something", name="inputBox")
        self.contentBox = ContentBox()
        self.header = Header(name="Welcome to TermApp", show_clock=True)
        self.friendsBox = FriendsBox()
        self.infoBox = InfoBox()

        self.commandBox = CommandBox(id="commandBox")
        self.commandBox.styles.display = "none"
        self.noticeBox = NoticeBox(id="noticeBox")
        self.noticeBox.styles.display = "none"
        self.tipBox = TipBox(id="tipBox")
        self.tipBox.styles.display = "none"

    def action_exit(self):
        exit(0)

    def action_display_noticeBox(self):
        self.set_focus(self.noticeBox.noticeList)
        self.noticeBox.styles.display = "block"

    def action_display_commandBox(self):
        self.set_focus(self.commandBox.inputBox)
        self.commandBox.styles.display = "block"

    def _action_remove_commandBox(self):
        self.set_focus(self.friendsBox.list)
        self.commandBox.styles.display = "none"

    def _action_remove_noticeBox(self):
        self.set_focus(self.friendsBox.list)
        self.noticeBox.styles.display = "none"

    def _action_remove_tipBox(self):
        self.set_focus(self.friendsBox.list)
        self.tipBox.styles.display = "none"

    def action_remove_box(self):
        if self.commandBox.styles.display == "block":
            self._action_remove_commandBox()
        elif self.noticeBox.styles.display == "block":
            self._action_remove_noticeBox()
        elif self.tipBox.styles.display == "block":
            self._action_remove_tipBox()

    def action_focus_friendsBox(self):
        self.set_focus(self.friendsBox)

    def action_focus_inputBox(self):
        self.set_focus(self.inputBox)

    def on_mount(self) -> None:
        self.install_screen(LoginBox(), name="login")
        self.install_screen(Welcome(), name="welcome")
        self.push_screen('login')

    @classmethod
    def runAll(cls, core):
        def run_app():
            app = cls(core)
            app.run()

        run_app()

    def compose(self) -> ComposeResult:
        yield self.header
        yield Horizontal(
            Vertical(
                self.friendsBox,
                self.infoBox,
                classes="test_border"
            ),
            Vertical(
                self.contentBox,
                self.inputBox,
                classes="vertical"
            ),
        )
        yield self.commandBox
        yield self.noticeBox
        yield self.tipBox

    def core_run(self):
        # 聚焦到下一个部件
        self.set_focus(self.inputBox)
        self.set_interval(0.1, self.server_listen)
        self.infoBox.title.text = self.username + ":boy_light_skin_tone:"
        self.core.run()

    def server_listen(self):
        if self.core.queue.qsize():
            message = self.core.queue.get()
            logging.debug(f"server listen: {message} {type(message)}")
            notify_sound()
            # ChatAll 消息处理
            if isinstance(message, ChatAllResponseMessage):
                if message.username == self.username:
                    self.contentBox.append(f"[bold red]{message.username}[/bold red] : {message.content}")
                else:
                    self.contentBox.append(f"[bold black]{message.username}[/bold black] : {message.content}")
            # 私聊消息处理
            elif isinstance(message, ChatToOneResponseMessage):
                from_user = message.from_user
                if self.contentBox.map.get(from_user) is None:
                    self.contentBox.map[from_user] = ""
                self.contentBox.map[from_user] += f"[bold black]{message.from_user}[/bold black] : {message.content}"

                if from_user == self.contentBox.label.text:
                    self.contentBox.update_list(from_user)
            elif isinstance(message, NoticeResponseMessage):
                from_user = message.from_user
                to_user = message.to_user
                logging.debug(f"{message}")
                # 发起请求阶段
                if message.notice_type == MessageTypes.NOTICE_FRIEND_REQ:
                    self.noticeBox.append(f"[bold red]{from_user}[/bold red] 想添加你为好友", name=from_user)
                # 添加成功阶段
                elif message.notice_type == MessageTypes.NOTICE_FRIEND_AGREE:
                    self.tipBox.content.text = f"好友[bold red]{from_user}[/bold red] 添加成功"
                    self.tipBox.styles.display = "block"
                    if message.reason != "not append":
                        self.friendsBox.append(f"[bold red]{from_user}[/bold red]", name=from_user)
                elif message.notice_type == MessageTypes.NOTICE_FRIEND_REFUSE:
                    self.tipBox.content.text = f"好友[bold red]{from_user}[/bold red] 拒绝了你的请求" + message.reason
                    self.tipBox.styles.display = "block"
                # 上线，接受好友列表
                elif message.notice_type == MessageTypes.NOTICE_FRIEND_LIST:
                    logging.debug(message.reason)
                    friends = message.reason[1:-1]
                    friends = friends.split(",")
                    for friend in friends:
                        friend = friend.strip()
                        self.friendsBox.append(f"[bold red]{friend}[/bold red]", name=friend)
                # 好友上、下线提示
                elif message.notice_type == MessageTypes.NOTICE_OFFLINE:
                    self.tipBox.content.text = f"好友[bold red]{from_user}[/bold red] 下线啦!"
                    self.tipBox.styles.display = "block"
                elif message.notice_type == MessageTypes.NOTICE_ONLINE:
                    self.tipBox.content.text = f"好友[bold red]{from_user}[/bold red] 上线啦!"
                    self.tipBox.styles.display = "block"
                # 好友删除功能提示
                elif message.notice_type == MessageTypes.NOTICE_FRIEND_REMOVE:
                    if from_user != "ChatAll":
                        self.tipBox.content.text = f"好友[bold red]{from_user}[/bold red]" + message.reason
                        self.tipBox.styles.display = "block"
                        self.friendsBox.remove_friend(from_user)
                    else:
                        self.tipBox.content.text = f"好友[bold red]{from_user}[/bold red] 不能删除"
                        self.tipBox.styles.display = "block"

    def on_tip_box(self, value):
        self.tipBox.content.text = value
        self.tipBox.styles.display = "block"

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.name == "inputBox":
            if event.value == "":
                self.on_tip_box("发送的消息不能为空")
                return
            to_user = self.contentBox.label.text
            if to_user == "ChatAll":
                logging.debug("APP: on_input_submitted")
                msg = ChatAllRequestMessage(event.value + "\n", self.username)
                self.core.send_msg(msg)
                self.inputBox.value = ""
            else:
                msg = ChatToOneRequestMessage(self.username, to_user, event.value + "\n")
                self.contentBox.append(f"[bold red]{self.username}[/bold red] : {event.value}\n")
                self.core.send_msg(msg)
                self.inputBox.value = ""


if __name__ == "__main__":
    pass
