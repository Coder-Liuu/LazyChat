<img src="https://s1.ax1x.com/2023/03/10/ppu2EAP.png" align="right" alt="Todo Icon" width="200" height="200">

# LazyChat 📨

LazyChat 是一款基于 TUI的用户聊天软件，它具有很棒的用户界面！
它实现了一些聊天软件的基本功能，如公共聊天室、添加好友、私聊等功能。

服务端从这里获取[LazyChat-Server](https://github.com/Coder-Liuu/LazyChat-server)

# Features 🌟

- 漂亮的终端界面
- 类似Vim的使用方式
- 💩一样的源代码

尽管有很多bug，但是我也不会修复 :)

# Installation 🔨

- pip一键安装

```
pip install git+https://github.com/Coder-Liuu/LazyChat.git
```

- 手动安装

```
git clone https://github.com/Coder-Liuu/LazyChat.git
cd LazyChat
pip install .
```

# screenshot 🖼️

[![ppu2t9U.png](https://s1.ax1x.com/2023/03/10/ppu2t9U.png)](https://imgse.com/i/ppu2t9U)
[![ppuRCCT.png](https://s1.ax1x.com/2023/03/10/ppuRCCT.png)](https://imgse.com/i/ppuRCCT)

# Usage ✋

```shell
lazychat -ip <server_ip> -p <server_port>
```
访问默认服务器：`lazychat -ip chat.thexb.fun`

|  界面   |    按键     |    功能    |
|:-----:|:---------:|:--------:|
| 通用按键  |    ESC    |  关闭提示框   |
|       |     q     |   退出程序   |
| 好友界面  |    TAB    |   切换焦点   |
|       |     /     |  命令行界面   |
|       |     m     |  查看消息通知  |
|       |     ?     |  说明说界面   |
|       |     j     | 移动到下一个好友 |
|       |     k     | 移动到上一个好友 |
|       |     l     | 与好友进行聊天  |
|       |     g     | 选择第一个好友  |
|       |     G     | 选择最后一个好友 |
|       |     d     |   删除好友   |
| 通知界面  | j|  选择下一条通知 |
|       |     k     | 选择上一条通知  |
|       |     l     |   同意请求   |
|       |     d     |   拒绝请求   |
| 说明书界面 | j |向下移动|
|       |k| 向上移动|
|       |g| 移动到顶部|
|       |G| 移动到底部|

# Contribution 🤝

始终对PR开放：）

此外本项目受到了[@kraanzu](https://github.com/kraanzu) [@lazygit](https://github.com/jesseduffield/lazygit)的项目启发，感谢他们这么好的创意！
