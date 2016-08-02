---
title: Tmux 学习摘要2--配置
date: 2016-07-30
writing-time: 2016-07-30 15:17--17:48
categories: programming
tags: Tmux
---

# 配置文件

系统范围的配置文件是 **/etc/tmux.conf**，而针对个人的配置文件在 **~/.tmux.conf**。

通过配置文件，可以定义新的快捷键，定义窗口、窗格布局等。


## 绑定 CAPS LOCK 键到 CTRL 键

在 OS X 上：打开 `Keyboard preference panel`->`System Preference`，按下 `Modifier` 键，然后将 `CAPS LOCK` 的动作改为 `Control`。

在 Linux，需对键盘配置文件进行修改：

```sh
sudo vi /etc/default/keyboard
```

找到以 **XKBOPTIONS** 开头的行，添加 `ctrl:nocaps` 使 `CAPS LOCK` 成为另一个 `CTRL` 键，或者添加 `ctrl:swapcaps` 使 `CAPS LOCK` 键和 `CTRL` 两键的功能相互交换。 例如，修改后的内容可能为：

```conf
XKBOPTIONS="lv3:ralt_alt,compose:menu,ctrl:nocaps"
```

然后运行：

```sh
sudo dpkg-reconfigure keyboard-configuration
```

详细请参考 [Emacs WIKI](www.emacswiki.org/emacs/MovingTheCtrlKey)。


## 定义一个更加容易按的 PREFIX

`CTRL-b` 不太好按，如果已将 CAPS LOCK 重定义为 CTRL，`CTRL-a` 会好按的多（GNU-SCreen 的PREFIX 也是 `CTRL-a`）。

*.tmux.conf* 中的配置命令是 **set-option** ，或者简写为 **set** 。

将 tmux PREFIX 重新定义：

```conf
set -g prefix C-a
```

这里的 `-g` 开关是 global 全局的意思，表示该设置值作用于所有的 tmux 会话。


可以使用 `unbind-key` 命令，或者简写的 `unbind` 命令来取消之前的绑定，如取消之前的 PREFIX 绑定 `CTRL-b`：

```conf
unbind C-b
```

因为重新绑定后，之前的绑定会自动取消，因此在本例中，没有必要用 `unbind`。


当配置文件 **.tmux.conf** 修改后，tmux 并不会自动进行重新读取和执行，需要在 tmux 会话中，使用快捷键 `PREFIX :` 进入命令模式，并执行 `source-file ~/.tmux.conf` 来重新加载配置文件 。

## 修改发送命令的默认延时时长

向 tmux 发送命令的默认延时时长非常短，可能会导致与 Vim 等编辑器冲突。

可以将延时时长调高些，以提高操作响应能力：

```conf
set -sg escape-time 1
```

窗口的默认编号是从 0 开始的，由于键盘上 0 和 1 的排列位置相关较远，，最好将窗口设置成从 1 开始编号：

```conf
set -g base-index 1
```

`set` 命令是针对会话的配置命令，而针对窗口的配置命令是 `set-window-option`，或者简写为 `setw`。由于窗格是窗口中的事物，要将窗格的默认编号也设置成从1 开始，应该用 `setw` 命令：

```
setw -g pane-base-index 1
```

# 自定义按键、命令和用户输入

tmux 的大部分快捷键都过长，或者难以操作。应该将常用的快捷键重新进行设置。

##　创建一个重新加载配置文件的快捷键

每次修改配置文件后，以前都需要执行 `source-file ~/.tmux.conf`，可以将这一命令定义成一个快捷键 `PREFIX r`：

```conf
bind r source-file ~/.tmux.conf
```

当重新加载后，最好要有消息提醒，可以用 `display` 命令在状态栏输出消息提醒。`bind` 命令可以绑定多条命令，各命令间用 `\;` 分开，如：

```conf
bind r source-file ~/.tmux.conf \; display "Reloaded!"
```

这样的绑定在使用时需要加前缀， 如果不要前缀，则：

```conf
bind-key -n C-r source-file ~/.tmux.conf
```

## 向会话内的应用发送 PREFIX

`CTRL-a` 也是 Vim, Bash 的快捷键，因此需要设置一个快捷键来向其它应用发送 `CTRL-a`：

```conf
bind C-a send-prefix
```

绑定后，只需按两次`CTRL-a` 就能向其它应用程序发送 `CTRL-a` 了。


## 窗格分割命令

默认的分割命令很难记，绑定能形象记忆的快捷键：

```conf
bind | split-window -h #水平分隔
bind - split-window -v
```

## 窗格间的移动

窗格间默认可以用 `PREFIX o` 进行循环切换，或者用 `PREFIX 方向键` 进行切换。参照 Vim， 用 hjkl 进行切换：

```conf
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
```

同时设置用 `PREFIX CTRL-h` 和 `PREFIX CTRL-l` 在窗口间进行切换移动：

```conf
bind -r C-h select-window -t :-
bind -r C-l select-window -t :+
```

这里的 `-r` 开关是 repeatable 可重复的意思，表示只需按一次 PREFIX, 后面可多次连续按绑定键。默认的间隔时间是 500 毫秒，可以设置 `repeat-time` 来修改。

## 设计修改窗格大小

```conf
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5
```

## 禁用鼠标

```conf
setw -g mode-mouse off
```

# 外观风格

## 颜色配置

确保 Tmux 和终端都支持 256 色。

在终端中测试是否支持 256 色：

```sh
$wget http://www.vim.org/scripts/download_script.php?src_id=4568 -O colortest.pl
$perl colortest.pl -w
```

在 Linux 上，可能需要在 .bashrc 中添加：

```sh
[ -z "$TMUX" ] && export TERM=xterm-256color
```
Mac Snow Leopard 的终端应用只支持 16 色， 需安装 iTerm2 支持更多颜色， 在 iTerm2 中，打开 `default profile`，将 `Terminal mode` 修改成 `xterm-256color`, 同时确保终端支持 UTF-8。

为使 tmux 能显示 256 色：

```sh
set -g default-terminal "screen-256color"
```

## 修改颜色

### 修改状态栏颜色

```sh
set -g status-fg white
set -g status-bg black
```

### 修改窗口列表颜色

```sh
setw -g window-status-fg cyan
setw -g window-status-bg default
setw -g window-status-attr dim

setw -g window-status-current-fg white
setw -g window-status-current-bg red
setw -g window-status-current-attr bright
```

### 修改窗格分隔栏颜色

```sh
set -g pane-border-fg green
set -g pane-border-bg black
set -g pane-active-border-fg white
set -g pane-active-border-bg yellow
```

### 定制命令行

```sh
set -g message-fg white
set -g message-bg black
set -g message-attr bright
```

# 定制状态栏

状态栏支持的变量

变量             | 描述
-----------------|
#H               | 本地主机名
#h               | 不含域名的主地主机名
#F               | 当前窗口符号
#l               | 当前窗口的索引号
#P               | 当前窗格的索引号
#S               | 当前会话名
#T               | 当前窗口的标题
#W               | 当前窗口的名称
##               | # 字符
#(shell-command) | Shell 命令的首行输出
#[attributes]    | 颜色或属性值设置


# 总结

命令总结

命令                              | 描述
----------------------------------|
set -g prefix C-a                 | 设置 PREFIX 键
set -sg escape-time n             | 设置按 PREFIX 键后，等待按键的毫秒数。
source-file [file]                | 重新加载配置文件
bind C-a send-prefix              | 按两次 PREFIX 将向其它应用发送 PREFIX 键组合
bind-key [key][command]           | 创建执行指定命令的快捷键，可简写为 bind
bind-key -r [key][command]        | 创建执行指定命令的快捷键，可简写为 bind，该快捷键可在一次按下 PREFIX 后，进行多次连续键入
unbind-key [key]                  | 取消快捷键绑定，可简写为 unbind
display-message 或 display        | 在状态栏显示信息
set-option [flags][option][value] | 为会话设置，使用 -g 开关为所有会话设置
set-window-option [option][value] | 设置窗口属性
set-a                             | 将设置值添加现有选项上，而不进行替换

来自 Pragmatic Tmux 的配置文件：

```conf
# workflows/tmux.conf
# Our .tmux.conf file

# Setting the prefix from C-b to C-a
set -g prefix C-a

# Free the original Ctrl-b prefix keybinding
unbind C-b

#setting the delay between prefix and command
set -sg escape-time 1

# Ensure that we can send Ctrl-A to other apps
bind C-a send-prefix

# Set the base index for windows to 1 instead of 0
set -g base-index 1

# Set the base index for panes to 1 instead of 0
setw -g pane-base-index 1

# Reload the file with Prefix r
bind r source-file ~/.tmux.conf \; display "Reloaded!"

# splitting panes
bind | split-window -h
bind - split-window -v

# moving between panes
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Quick pane selection
bind -r C-h select-window -t :-
bind -r C-l select-window -t :+

# Pane resizing
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# mouse support - set to on if you want to use the mouse
setw -g mode-mouse off
set -g mouse-select-pane off
set -g mouse-resize-pane off
set -g mouse-select-window off

# Set the default terminal mode to 256color mode
set -g default-terminal "screen-256color"

# enable activity alerts
setw -g monitor-activity on
set -g visual-activity on

# set the status line's colors
set -g status-fg white
set -g status-bg black

# set the color of the window list
setw -g window-status-fg cyan
setw -g window-status-bg default
setw -g window-status-attr dim

# set colors for the active window
setw -g window-status-current-fg white
setw -g window-status-current-bg red
setw -g window-status-current-attr bright

# pane colors
set -g pane-border-fg green
set -g pane-border-bg black
set -g pane-active-border-fg white
set -g pane-active-border-bg yellow

# Command / message line
set -g message-fg white
set -g message-bg black
set -g message-attr bright

# Status line left side
set -g status-left-length 40
set -g status-left "#[fg=green]Session: #S #[fg=yellow]#I #[fg=cyan]#P"

set -g status-utf8 on

# Status line right side
# 15% | 28 Nov 18:15
set -g status-right "#(~/battery Discharging) | #[fg=cyan]%d %b %R"

# Update the status bar every sixty seconds
set -g status-interval 60

# Center the window list
set -g status-justify centre

# enable vi keys.
setw -g mode-keys vi

# Open panes in the same directory using the tmux-panes script
unbind v
unbind n
bind v send-keys " ~/tmux-panes -h" C-m
bind n send-keys " ~/tmux-panes -v" C-m

# Maximize and restore a pane
unbind Up
bind Up new-window -d -n tmp \; swap-pane -s tmp.1 \; select-window -t tmp
unbind Down
bind Down last-window \; swap-pane -s tmp.1 \; kill-window -t tmp

# Log output to a text file on demand
bind P pipe-pane -o "cat >>~/#W.log" \; display "Toggled logging to ~/#W.log"
```

参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
