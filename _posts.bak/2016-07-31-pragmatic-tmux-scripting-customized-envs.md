---
title: Tmux 学习摘要3--使用脚本定制 tmux 环境
date: 2016-07-31
writing-time: 2016-07-31 21:31--22:54
categories: programming
tags: Tmux
---

使用脚本为每个项目定制一个 tmux 环境：创建会话，分割窗口，自动开启项目要用到的程序等。

# 使用 tmux 命令创建定制设置

可以使用 tmux 命令在一个会话中分割窗口，改变布局，甚至开启程序。完成这些操作的关键是使用 `-t` target 开关。

当有一个命名 tmux 会话后，可以这样与它进行关联：

```sh
$ tmux attach -t [session_name]
```

我们使用 `-t` 开关将命令导向到相应的 tmux 会话。假设新建了一个命名为  **development** 的会话：

```sh
$ tmux new -s development
```

可以通过 tmux 命令对其窗口进行水平分割：

```sh
$ tmux split-window -h -t development
```

当与该会话关联后，可以看到该会话的窗口被分割成了水平两个窗格了。

## 使用脚本配置项目开发环境

通过脚本来创建一个会话，创建窗口和窗格，然后在每个窗格中启动一些程序。

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

使用 `-s` 开关指定会话的名字为 development，使用 `-n` 开关指定该会话的初始窗口名称为 editor，使用 `-d` 开关使得创建后立即与其脱离。

当启动会话后，将工作目录切换到项目目录上，如 *devproject*。在脚本文件中使用 tmux 的 **send-keys** 来改变目录：

```sh
# scripting/development
tmux send-keys -t development 'cd ~/devproject' C-m
```

行末的 **C-m** 是 **CTRL-m** ，表示发送一个回车键。类似地，可以在该窗口中开启一个 Vim 编辑器：

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

每个窗口都有一个编号，其基编号由 `set base-index` 设置，而窗口中的每个窗格也有一个编号，其基编号由 `setw pane-base-index` 设置。要指定特定的窗口和窗格，使用格式： `[session]:[window].[pane]`，如 `development:1.2`。因此，在会话的首窗口的第二个窗格中切换到项目目录：

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

该方式只适用于某个具体项目。

# 通过 tmux 配置文件设置项目开发环境

**.tmux.conf** 文件本身可以包含命令来设置默认环境。通过上面相同的命令，可以在配置文件中设置每个开发环境的通用配置。

tmux 还可以通过 `-f` 开关来指定配置文件，从而我们可以在每个项目中创建一个专门的配置文件，并在其中设置窗口窗格、快捷键等。

首先创建一个新的配置文件 **app.conf**，并使用上面类似的命令。由于当前是在一个 tmux 配置文件中，所以所有的命令都不再需要使用 tmux 前缀。配置文件的内容：

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


# 使用 tmuxinator 管理配置

tmuxinator 是一个用于编写和管理不同 tmux 配置文件的小工具。我们在 YAML 文件中定义窗口布局和命令，然后用 **tmuxinator** 来加载。tmuxinator 可以对配置文件进行集中管理，并且易于创建复杂布局。通过它还可以指定每个窗口开启前需执行的命令。

tmuxinator 依赖 Ruby。

通过 Rubygems 安装：

```sh
$sudo gem install tmuxinator
```

tmuxinator 需要有 **EDITOR** 环境变量，可以在 Linux 的 *.bashrc* 或 OS X 的 *.bash_profile* 上设置：

```sh
export EDITOR=vim
```

创建一个 tmuxinator 项目 development:

```sh
$ tmuxinator open development
```

执行后会用你的编辑器显示项目的默认配置信息，如：

```yaml
#scripting/default.yaml
project_name: Tmuxinator
project_root: ~/code/rails_project
socket_name: foo # Not needed. Remove to use default socket
rvm: 1.9.2@rails_project
pre: sudo /etc/rc.d/mysqld start
tabs:
  - editor:
    layout: main-vertical
    panes:
      - vim
      - #empty, will just run plain bash
      - top
  - shell: git pull
  - database: rails db
  - server: rails s
  - logs: tail -f logs/development.log
  - console: rails c
  - capistrano:
  - server: ssh me@myhost
```

该 YAML 文件定义了一个 tmux 会话，其中有 8 个窗口。第一个窗口中有 3 个窗格，使用 *main-vertical* 布局。其它的窗口都开启和运行了各种的服务和程序。同时，还可以指定在每个窗口加载时会自动运行的命令。

先创建一个开发环境，其中 Vim 在上面，一个终端在下面：

```yaml
#scripting/development.yaml, Tmuxinator 0.8.1
name: devproject
root: ~/devproject
windows:
  - editor:
      layout: main-horizontal
      panes:
        - vim
        - #empty, will just run plain bash
  - console: # empty
```

YAML 文件使用 2 个空格表示缩进。

开启该环境：

```sh
$tmuxinator development
```

tmuxinator 会自动加载默认的 *.tmux.conf* 文件，然后再执行我们在 YAML 文件中指定的配置信息。

重新打开配置文件修改：

```sh
$tmuxinator open development
```

配置文件默认都存放在 **~/.tmuxinator/** 目录下。tmuxinator 实质上是根据我们的配置文件生成脚本命令文件，然后再一一执行其中的命令。


# 总结

## 可用于脚本中的 tmux 命令

命令                                              | 描述
--------------------------------------------------|
tmux new-session -s development -n editor         | 创建一个命名为 **development** 的会话，并且命名首窗口为 **editor**
tmux attach -t development                        | 关联到命名窗口 **development**
tmux send-keys -t development '[keys]' C-m        | 向命名会话 **development** 中的活动窗口或窗格发送按键，`C-m` 相当于回车键
tmux send-keys -t development:1.0 '[keys]' C-m    | 向命名会话 **development** 中的第 1 个窗口中的第 0 个 窗格发送按键，`C-m` 相当于回车键
tmux select-window -t development:1               | 使命名会话 **development** 中的第 1 个窗口成为活动窗口
tmux split-window -v -p 10 -t development         | 将命名会话 **development** 中的当前窗口垂直分割，其中下面的窗格高度占 10%
tmux select-layout -t development main-horizontal | 为命名会话 **development** 选择布局
tmux -f app.conf attach                           | 加载 *app.conf* 配置文件，并关联到该配置文件生成的会话


## tmuxinator 命令

命令                                   | 描述
---------------------------------------|
tmuxinator open [name]                 | 在默认编辑器中打开或创建一个项目配置文件
tmuxinator [name]                      | 加载并运行该项目配置文件，创建（如果还没有创建）并关联创建的会话
tmuxinator list                        | 列出当前所有的项目
tmuxinator copy [source] [destination] | 复制项目配置文件
tmuxinator delete [name]               | 删除项目配置文件
tmuxinator implode                     | 删除所有当前的项目配置文件
tmuxinator doctor                      | 诊断 tmuxinator 及系统中的配置文件



参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
