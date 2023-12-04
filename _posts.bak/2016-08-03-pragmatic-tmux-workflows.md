---
title: Tmux 学习摘要6--工作流
date: 2016-08-03
writing-time: 2016-08-03 12:14--15:30
categories: programming
tags: Tmux
---

# 高效使用窗口和窗格

## 将窗格转变成窗口

将当前窗格升级为一个独立的窗口，使用快捷键 `PREFIX !`，此后，当前会话中会多出一个窗口。

## 将窗口转变成一个窗格

在命令模式下使用 `join-pane` 命令，该命令的格式为：

```sh
join-pane -s [souce-window-no] -t [target-window-no]
```

`-s` 和 `-t` 两个参数都可以忽略，表示为当前的窗口或窗格。


## 最大化窗格与还原

将当前窗格放大，放在一个独立的窗口中显示，查看完之后再还原。

实现此功能，先将当前的窗格通过 `break-pane` 命令分离出来，再将它放到一个临时的窗口中显示。将该操作绑定到方向键上：

```sh
unbind Up
bind Up new-window -d -n tmp \; swap-pane -s tmp.1 \; select-window -t tmp
```

它使用 `swap-pane` 命令实现窗格的互换。 同理，要将窗口从当前的临时窗口还原到的原来窗口，还是使用 `swap-pane` 命令，并绑定到方向键：

```sh
unbind Down
bind Down last-window \; swap-pane -s tmp.1 \; kill-window -t tmp
```

由于它是使用 `last-window` 来查找原来的窗口，因此有一定的缺陷，我们在放大查看后，不可切换到其它窗口，只能立即还原回来。

## 在创建窗口和窗格时启动命令

可以指定 tmux 在创建会话中的第一个窗口时启动什么命令，命令写在创建会话的最后，如：

```sh
$ tmux new-session -s servers -d "ssh deploy@burns"
```

也可以在创建窗格时指定启动什么命令，如：

```sh
$ tmux split-window -v "ssh dba@smithers"
```

但是这两种方式指定的自动启动命令，当命令结果或退出后，其关联的窗口或窗格也会自动关闭。

# 会话管理

## 在会话间移动

一台机器上的所有会话都由同一个 tmux 服务器管理。而每个开启会话的终端只是一个 tmux 客户端。我们使用 `switch-client` 命令在各会话间进行切换。或者使用快捷键 `PREFIX (` 和 `PREFIX )` 在各会话间进行切换关联。也可以用 `PREFIX s` 列出所有的会话，供我们选择后切换。


## 创建或者关联到一个现有会话

可以使用 `has-session` 命令进行判断，只有当会话不存在时才创建会话：

```sh
if ! tmux has-session -t remote; then
    exec tmux new-session -s development -d
    # other setup commands before attaching ...
fi
exec tmux attach -t development
```


# 在会话间移动窗口

可以将一个会话中的窗口移到到另一个会话中。使用 `move-window` 命令，该命令绑定到快捷键 `PREFIX .`，可以按下该快捷键，选择要移动的窗口，然后输入目标会话名。例如：

先创建两个会话：

```sh
$ tmux new -s editor -d vim
$ tmux new -s processes -d top
```

关联到 processes 会话，在其中按下 `PREFIX .` ，然后在命令行中输入 editor，此时会将 processes 会话中的唯一窗口移到 editor 会话中，这些意味着 processes 会话将会关闭。移动窗口对应的命令如下：

```sh
$ tmux move-window -s processes:1 -t editor
```

# tmux 与操作系统

使 tmux 与操作系统紧密集成。

## 使用不同的 Shell

默认使用的是 bash, 如果要改成 zsh，可以在 *.tmux.conf* 中配置：

```conf
set -g default-command /bin/zsh
set -g default-shell /bin/zsh
```

## 启动终端时自动运行 tmux

可以在 Linux 上的 *.bashrc* 或者 OS X 上的 *.bash_profile* 上进行配置，并将会话设置为用户名：

```sh
if [[ "$TERM" != "screen-256color" ]]
then
    tmux attach-session -t "$USER" || tmux new-session -s "$USER"
    exit
fi
```


## 将程序的输出记录到日志文件

使用 `pipe-pane` 命令将窗格的输出保存到一个文件中，在命令模式下开启该功能：

```sh
pipe-pane -o "mylog.txt"
```

当使用相同的参数重新执行时，输出保存到日志的功能会被关闭，即该功能像一个开关。

可以将它绑定到一个快捷键：

```sh
bind P pipe-pane -o "cat >>~/#W.log" \; display "Toggled logging to ~/#W.log"
```


参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
