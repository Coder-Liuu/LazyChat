from textual import events
from textual.app import ComposeResult, App
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from rich.markdown import Markdown
from textual.widgets import Welcome

WELCOME_MD = """
# Welcome LazyChat !

LazyChat是基于[Textual](https://github.com/Textualize/textual)一款终端聊天应用程序。
如果您熟悉Vim操作和喜欢使用终端来进行聊天，那么LazyChat将是您的不二选择。

## Manual

---
- 通用按键
    - ESC      关闭提示框       
    - q        退出程序
- 好友界面
    - TAB      切换焦点
    - /        命令行界面        
    - m        查看消息通知        
    - ?        说明说界面
    - j        移动到下一个好友   
    - k        移动到上一个好友   
    - l        与好友进行聊天    
    - g        选择第一个好友
    - G        选择最后一个好友
    - d        删除好友        
- 通知界面
    - j        选择下一条通知
    - k        选择上一条通知
    - l        同意请求
    - d        拒绝请求
- 说明书界面
    - j        向下移动
    - k        向上移动
    - g        移动到顶部
    - G        移动到底部
---
     
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
            color: $text;
        }

        Welcome text {
            margin:  0 1;
        }
        a:hover {color:pink;}
    """
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    view = Container(Static(Markdown(WELCOME_MD), classes="text"))

    def compose(self) -> ComposeResult:
        yield self.view

    def on_key(self, event: events.Key):
        key = event.character
        if key in ["j", "down"]:
            self.view.scroll_down()
        elif key in ["k", "up"]:
            self.view.scroll_up()
        elif key in ["home", "g"]:
            self.view.scroll_home()
        elif key in ["end", "G"]:
            self.view.scroll_end()


if __name__ == '__main__':
    class WelcomeApp(App):
        def compose(self) -> ComposeResult:
            yield Welcome()

        def on_button_pressed(self) -> None:
            self.exit()


    app = WelcomeApp()
    app.run()
