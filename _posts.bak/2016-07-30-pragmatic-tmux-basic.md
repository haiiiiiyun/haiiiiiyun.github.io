---
title: Tmux 学习摘要1--使用默认配置进行基本操作
date: 2016-07-30
writing-time: 2016-07-30 11:00--12:27
categories: programming
tags: Tmux
---

tmux 是一个运行于 OS X 和 Unix 上的终端分屏软件 *terminal multiplexer*。

# 快捷键的表示及按键规则

+ `CTRL-b`: 同时按下 `CTRL` 键和 `b` 键
+ `CTRL-R`: 同时按下 `CTRL`、`SHIFT` 和 `r` 键
+ `CTRL-b d`: 同时按下 `CTRL` 键和 `b` 键，再松开，然后再迅速按下 `d` 键


# 安装

在 OS X 上：

```sh
$ brew install tmux
```

在 Debian 和 Ubuntu 上：

```sh
$ sudo apt-get install tmux
```

确定是否安装成功：

```sh
$ tmux -V
```

# 开启 tmux

开启 tmux 只需输入命令：

```sh
$ tmux
```

执行后会打开一个 tmux 会话，和普通的终端会话一样，可以在里面输入和执行任何命令。

要想从该 tmux 会话中退回到普通的终端，输入命令：

```sh
$ exit
```

以上的使用方式用处不大，应该使用 “命名会话”。

## 创建命名会话

一台机器上可以有多个会话，要使各会话组织有序，应对其命名。

创建一个命名为 *basic* 的会话：

```sh
$ tmux new-session -s basic
```

也可以用简写的命令：

```sh
$ tmux new -s basic
```

# 脱离和关联会话

tmux 是一个 CS 模式的程序，当开启一个 tmux 会话时，会话就是一个服务器。所有在该会话环境中开启的程序和进程都由这个会话服务器管理。当你与该会话 “脱离” 时，由于会话还没有结束，这些开启的程序和进程都会在后台继续运行。之后，我们可以重新 “关联” 该会话，继续之前的工作。

示例：

先创建一个命名会话：

```sh
$ tmux new -s basic
```

在该会话中，开启一个 *top* 命令：

```sh
$ top
```

然后使用快捷键 `CTRL-b d` 从当前会话中脱离出来，脱离后，会回到普通的终端中。

`CTRL-b d` 快捷键的正确按法是：先同时按下 `CTRL` 键和 `b` 键作为 tmux 命令的前缀，再全部松开按键，然后迅速按下代表 tmux 命令的 `d` 键，将 d 命令发送给 tmux。

## 命令前缀

tmux 的默认命令前缀是 `CTRL-b`，记为 `PREFIX`，可以对该设置进行再绑定。


## 重新关联到现有的会话

列出当前机器上的全部会话：

```sh
$ tmux list-sessions
```

也可以用简写命令：

```sh
$ tmux ls
```

该命令会显示当前只有一个会话：

```
basic: 1 windows (created Sat Jul 30 09:48:32 2016) [80x23]
```

要想关联现有的会话，如果只有一个会话的话，直接：

```sh
$ tmux attach
```

先用 `PREFIX d` 从当前会话脱离，再创建一个新的会话但不自动关联：

```sh
tmux new -s second_session -d
```

此时罗列会话命令会出来有两个会话：

```sh
tmux ls
```

```
basic: 1 windows (created Sat Jul 30 09:48:32 2016) [80x23]
second_session: 1 windows (created Sat Jul 30 09:52:31 2016) [80x23]
```

可以用 `-t` (target?) 选项来指定关联的会话：

```sh
$ tmux attach -t second_session
```

## 关闭会话

在 tmux 会话内部，可以用 `exit` 命令直接销毁和退出当前会话。在普通终端下也可以用 `kill-session` 进行：

```sh
$ tmux kill-session -t basic
$ tmux kill-session -t second_session
```

如果某个会话中有僵死的程序，可以用这个方法来关闭整个会话。

# 多窗口操作

在一个 tmux 会话中可以同时运行多个程序，tmux 在会话中可以使用多窗口对多个程序进行有序组织和管理。

当开启一个会话时，会自动创建一个初始窗口，之后，在会话中可以再创建更多的窗口。

创建一个命名为 **windows** 的会话，并将第一个（默认）窗口命名为 **shell**：

```sh
$ tmux new -s windows -n shell
```

## 在会话中创建一个新窗口

在会话中，使用快捷键 `PREFIX c` 创建一个新的窗口。并在该窗口中运行 `top` 命令。注意到，该窗口的名称是基于运行的程序而动态变化的。为方便管理，应对其显式命名，方法是在使用快捷键 `PREFIX ,` 后，在状态栏中输入名称，如 Processes。


## 在会话中的窗口间切换

当前焦点窗口的窗口名上会有一个 `*` 号。窗口切换可以用以下快捷键：

+ `PREFIX n`: 移到下一个（可往复循环）
+ `PREFIX p`: 移到上一个（可往复循环）
+ `PREFIX 编号`: 直接移到某编号的窗口，如 `PREFIX 0`
+ `PREFIX f`: 根据窗口名来定位
+ `PREFIX w`: 显示出一个含有所有窗口名称的列表窗口，供选择切换

要关闭当前窗口，在窗口中直接运行 `exit` 命令。也可以用快捷键 `PREFIX &`，它会在状态栏进行确认操作。当所有窗口都关闭后，会话也随之关闭。


# 多窗格操作

一个窗口可以分割成多个窗格。并在每个窗格中运行不同程序。


创建一个新的会话，练习多窗格操作：

```sh
$ tmux new -s panes
```

窗格分割快捷键：

+ `PREFIX %`: 水平平均分割
+ `PREFIX "`: 垂直平均分割

在各窗格间切换焦点，用快捷键 `PREFIX o`，也可以用 `PREFIX 方向键` 进行切换。


## 窗格布局模板

内置的几种布局模板：

+ even-horizontal: 从左到右水平平均布局
+ even-vertical: 从上到下垂直平均布局
+ main-horizontal: 上侧一个大窗格，其它的在下边
+ main-vertical: 左侧一个大窗格，其它的在右边
+ tiled: 所有窗格在屏幕上平均布局

可以用快捷键 `PREFIX SPACEBAR` 依次在各布局模板间切换。

## 关闭窗格

用快捷键 `PREFIX x`。


# 使用命令模式

当前使用的快捷键都是 tmux 命令的快捷键。tmux 命令即可以在终端命令行中运行，也可以和 VI 类似，在命令模式下的状态行中运行。

在会话中，进入命令模式用快捷键 `PREFIX :`, 此时，可以在状态栏中运行相应的 tmux 命令，如创建一个命名为 console 的新窗口： `new-window -n console`。

创建一个命名窗口，同时执行 "top" 命令： `new-window -n processes "top"`，这样创建的窗口当窗口中的命令执行完毕后，窗口会自动关闭。

# 总结

快捷键 `PREFIX ?` 列出所有的快捷键。

创建会话的命令：

命令                        | 描述
----------------------------|
tmux new-session            | 创建一个匿名会话，可以简写为 `tmux new` 或直接 `tmux`
tmux new -s devel           | 创建一个命名为 "devel" 的会话
tmux new -s devel -n editor | 创建一个名称为 "devel" 的会话，且将第一个窗口命名为 "editor"
tmux attach -t devel        | 关联到名为 "devel" 的会话


关于会话、窗口、窗格的默认命令

命令         | 描述
-------------|
PREFIX d     | 脱离会话，会话会在后台继续运行
PREFIX :     | 进入命令模式
PREFIX c     | 在会话中创建一个新窗口，对应 tmux 命令 `new-window`
PREFIX 0...9 | 根据窗口编号在窗口中切换
PREFIX w     | 显示出当前会话中所有的窗口，供选择切换
PREFIX ,     | 命名当前窗口
PREFIX &     | 关闭当前窗口
PREFIX %     | 水平平均分割窗口
PREFIX "     | 垂直平均分割窗口
PREFIX o     | 在多个窗格间循环切换
PREFIX q     | 显示窗格的编号
PREFIX x     | 关闭当前窗格
PREFIX SPACE | 在各窗格布局前切换

参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
