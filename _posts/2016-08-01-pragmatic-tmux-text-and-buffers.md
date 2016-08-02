---
title: Tmux 学习摘要4--处理文本和缓冲区
date: 2016-08-01 16:30
writing-time: 2016-08-01 16:30--22:54
categories: programming
tags: Tmux
---

# 在复制模式下移动

当进行测试或者查看日志文件时，由于内容较多，往往需要进行上下翻滚查找。

按下 `PREFIX [` 进入复制模式，然后可以在屏幕上使用方向键进行移动了。要想使用 Vim 的各种移动键进行移动，可以在 *.tmux.conf* 中配置：

```conf
setw -g mode-keys vi
```

使用 `PREFIX [` 后进入的复制模板，相当于 Vim 中使用 `ESC` 进入的 Normal 模式，在其中可以用 `hjkl`，`wbfF`, `Ctrl-b` 等进行移动，使用 `?/` 等进行查询等。

退出复制模式默认使用回车键。

# 复制粘贴文本

在复制模式下，按下空格键进入文本选取状态，然后使用 Vim 的移动命令进行移动选取，当按下回车键后，所选取的文本将被复制到一个粘贴缓冲区。

在复制模式下，按 `PREFIX ]` 将当前粘贴缓冲区中的内容粘贴出来。

## 获取窗格内容

将一个窗格里可见的所有内容复制到一个粘贴缓冲区中：先按 `PREFIX :` 进入命令模式，然后运行 `capture-pane` 命令。

## 显示和保存缓冲区

显示缓冲区的内容：

```sh
$ tmux show-buffer
```

使用 **save-buffer** 命令将缓冲区中的内容保存到一个文件中，例如，可以先将一个窗格中的所有内容复制到缓冲区，然后将缓冲区的内容保存到文件中：

```sh
$ tmux capture-pane && tmux save-buffer buffer.txt
```

或者在 tmux 会话的命令模式下：

```sh
:capture-pane;save-buffer buffer.txt
```

可以将这两条命令映射成一个快捷键。

## 使用多个缓冲区

tmux 的缓冲区和系统的不同，它的缓冲区类似一个堆栈，新复制的内容在堆栈的顶部，而不会直接覆盖已存在的缓冲区内容。

当按下 `PREFIX ]` 时，默认问题粘贴最顶部的缓冲区的内容，即缓冲区 0 的内容，也可以在命令模式下通过 **choose-buffer** 命令选取要粘贴的缓冲区，选取后按回车键完成粘贴。

这些缓冲区内容在不同的会话间都可以共享。

## 重新绑定复制和粘贴键

将复制粘贴操作参照 Vim 的模式进行改造，如按 `ESC` 键切换复制模式，使用 `y` 进行复制，使用 `v` 开始选取文本，使用 `p` 进行粘贴：

```conf
unbind [
bind Escape copy-mode
unbind p
bind p paste-buffer
bind -t vi-copy 'v' begin-selection
bind -t vi-copy 'y' copy-selection
```

# 在 Linux 上使用系统粘贴板

在 Ubunut 上，通过 [xclip](http://sourceforge.net/projects/xclip/) 工具可以将 tmux 缓冲区与系统的粘贴板整合起来，从而使得程序间的文本复制粘贴更加容易。

安装 **xclip** ：

```sh
$ sudo apt-get install xclip
```

然后可以将 tmux 的 **save-buffer** 和 **set-buffer** 命令与 **xclip** 结合起来。

将当前缓冲区的内容复制到系统的粘贴板，可以在 **.tmux.conf** 文件中进行绑定：

```conf
bind C-c display "Copied" \; run "tmux save-buffer - | xclip -i -sel clipboard"
```

将系统粘贴板中的内容粘贴到当前位置：

```conf
bind C-v run "tmux set-buffer \"$(xclip -o -sel clipboard)\"; tmux paste-buffer"
```


## 快捷键

快捷键    | 描述
----------|
PjREFIX [ | 进入复制模式
PREFIX ]  | 粘贴当前缓冲区中的内容
PREFIX =  | 先列出所有粘贴缓冲区的内容，然后粘贴选中的缓冲区内容


## 命令

命令                   | 描述
-----------------------|
show-buffer            | 显示当前缓冲区的内容
capture-pane           | 将当前窗格中的所有可见内容得到最顶部的缓冲区
list-buffers           | 列出所有缓冲区的内容
choose-buffer          | 列出所有缓冲区，选取其中一个进行粘贴
save-buffer [filename] | 将缓冲区的内容保存到文件


参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
