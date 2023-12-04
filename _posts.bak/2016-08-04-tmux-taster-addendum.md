---
title: Tmux 学习摘要7--补遗
date: 2016-08-04
writing-time: 2016-08-03 16:17--2016-08-04 14:37
categories: programming
tags: Tmux
---

`PREFIX ?`: 列出所有的快捷键，它对应的命令行命令为 `:list-keys`。

`:list-commands` 列出所有的 tmux 命令。

`:info` 命令显示有关当前会话的信息:w。


将命令前缀改为 `CTRL-SPACE` 更加容易使用，但是输入法切换可能也会用这两个键，因此要进行修改设置。

```sh
unbind C-b
set -g prefix C-Space
```


方便切换到上一个窗口。

```sh
bind-key L last-window
```

`：resize-pane -Z` 命令将当前窗格进行最大化，当再次运行时，会还原到原来的大小，可以将它绑定到快捷键 `PREFIX z`。


`PREFIX !` 将当前窗格移到一个新的窗口中。


`PREFIX }` 将当前窗格在窗口中顺时针改变位置， `PREFIX {` 是逆时针。

`PREFIX SPACE` 轮换调整当前窗口的布局。


同步会话中多个窗格中的输入：

```sh
:setw synchronize-panes on
```

`PREFIX w` 或者 `:choose-window` 列出所有窗口供选择切换。


在两个会话间共享窗口：

```sh
:link-window -t [session.windoid]
```


参考资源：

[tmux Taster](http://www.apress.com/9781484207765)
