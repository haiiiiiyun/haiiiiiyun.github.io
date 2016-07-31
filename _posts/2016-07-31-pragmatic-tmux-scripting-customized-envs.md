---
title: Tmux 学习摘要3--使用脚本定制 tmux 环境
date: 2016-07-31
writing-time: 2016-07-31 21:31--22:54
categories: programming
tags: Tmux
---

使用脚本为每个项目定制一个 tmux 环境：创建会话，分割窗口，自动开启项目要用到的程序等。

# 使用 tmux 命令创建一个定制的设置

可以通过 tmux 命令在一个会话中分割窗口，改变布局，甚至开启程序。完成这些操作的关键是使用 `-t` target 开关。

当有一个命名的 tmux 会话后，可以这样与它进行关联：

```sh
$ tmux attach -t [session_name]
```

我们使用 `-t` 开关将命令导向到相应的 tmux 会话。假如新建了一个 **development** 的会话：

```sh
$ tmux new -s development
```

我们可以通过 tmux 命令对其窗口进行水平分割：

```sh
$ tmux split-window -h -t development
```

当与该会话关联后，可以看到该会话的窗口为分割成了水平两个窗格了。

## 使用脚本来配置项目开发环境

通过脚本来创建一个会话，创建窗口及窗格，然后在每个窗格中启动一些程序。

先在 home 目录下创建一个 **development** 的脚本，并设置为可执行：

```sh
$touch ~/development
$chmod +x ~/development
```

在该脚本文件中，首先创建一个命名为 **development** 的 tmux 会话：

```sh
# scripting/development
tmux new-session -s development -n editor -d
```

使用 `-s` 开关指定会话的名字为 development，使用 `-n` 开关指定该会话的初始窗口的名称为 editor，使用 `-d` 开关使得创建后立即与其脱离。

当启动会话后，应该把工作目录切换到项目目录上，如 *devproject*。在脚本文件中使用 tmux 的 **send-keys** 来改变目录：

```sh
# scripting/development
tmux send-keys -t development 'cd ~/devproject' C-m
```

行末的 **C-m** 是 **CTRL-m** ，表示最后发送一个回车键。类似地，可以在该窗口中开启一个 Vim 编辑器：

```sh
# scripting/development
tmux send-keys -t development 'vim' C-m
```

分割主编辑器窗口，使其下面有一个小的终端窗口，可以使用 split-window 命令：

```sh
# scripting/development
tmux split-window -v -t development
```

也可以指定分割窗格所占的百分比：

```sh
# scripting/development
tmux split-window -v -p 10 -t development
```

也可以选择窗口使用的布局：

```sh
# scripting/development
tmux select-layout -t development main-horizontal
```

此时，可以对首窗口进行分割和发送命令了。

## 向指定的窗口和窗格发送命令

每个窗口都有一个编号，其基编号由 `set base-index` 设置，而窗口中的每个窗格也有一个编号，其基编号由 `setw pane-base-index` 设置。要指定特定的窗口和窗格，使用格式： `[session]:[window].[pane]`，如 `development:1.2`。因此，实现在会话的首窗口的第二个窗格中切换到项目目录：

```sh
# scripting/development
tmux send-keys -t development:1.2 'cd ~/devproject' C-m
```

## 创建和选择窗口

创建一个全屏的终端窗口，使用 **new-window** 命令：

```sh
# scripting/development
tmux new-window -n console -t development
tmux send-keys -t development:2 'cd ~/devproject' C-m
```

在新建窗口后，进行了目录切换，由于新窗口只有一个窗格，所以无需指定窗格号。

当开启会话后，需要将首个窗口显示出来，使用 **select-window** 命令：

```sh
# scripting/development
tmux select-window -t development:1
tmux attach -t development
```

在该脚本中，可以继续增加内容：增加窗口和窗格，开启到服务器的远程连接、打开日志文件、开启数据库命令行、更新代码库，……

该例中的脚本全部内容如下：

```sh
tmux new-session -s development -n editor -d
tmux send-keys -t development 'cd ~/devproject' C-m
tmux send-keys -t development 'vim' C-m
tmux split-window -v -t development
tmux select-layout -t development main-horizontal
tmux send-keys -t development:1.2 'cd ~/devproject' C-m
tmux new-window -n console -t development
tmux send-keys -t development:2 'cd ~/devproject' C-m
tmux select-window -t development:1
tmux attach -t development
```

并用以下命令执行：

```sh
$ ~/development
```

该脚本每次运行都会生成一个新的会话，当该会话存在时，再运行该脚本会出错，可以用 **has-session** 命令解决：

```sh
tmux has-session -t development
if [ $? !=0 ]
    tmux new-session -s development -n editor -d
    tmux send-keys -t development 'cd ~/devproject' C-m
    tmux send-keys -t development 'vim' C-m
    tmux split-window -v -t development
    tmux select-layout -t development main-horizontal
    tmux send-keys -t development:1.2 'cd ~/devproject' C-m
    tmux new-window -n console -t development
    tmux send-keys -t development:2 'cd ~/devproject' C-m
    tmux select-window -t development:1
fi
tmux attach -t development
```

该方式只适合用于某个具体项目。

# 通过 tmux 配置文件设置项目开发环境

**.tmux.conf** 文件本身可以包含命令来设置默认环境。通过上面相同的命令，可以把在其中设置每个开发环境都需要的配置。

tmux 还可以通过 `-f` 开关来指定配置文件，从而我们可以在每个项目中创建一个专门的配置文件，并在其中设置窗口窗格、快捷键等。

产自创建一个新的配置文件 **app.conf**，并使用上面类似的命令。由于当前是在一个 tmux 配置文件中，所以所有的命令都不再需要使用 tmux 前缀。配置文件的内容：

```conf
# scripting/app.conf
source-file ~/.tmux.conf
new-session -s development -n editor -d
send-keys -t development 'cd ~/devproject' C-m
send-keys -t development 'vim' C-m
split-window -v -t development
select-layout -t development main-horizontal
send-keys -t development:1.2 'cd ~/devproject' C-m
new-window -n console -t development
send-keys -t development:2 'cd ~/devproject' C-m
select-window -t development:1
```

首行通过加载默认的 ~/.tmux.conf 文件，完成了所有的默认配置。

开启命令：

```sh
$ tmux -f app.conf attach
```

上面的 tmux 最后有 **attach** 命令是因为： tmux 开启时默认总是会运行 **new-session** 命令，但是我们的配置文件中已经新建了一个会话，因此通过使用 **attach** 避免会出现两个会话。

这种方法比较灵活，但是配置文件会较多。

参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
