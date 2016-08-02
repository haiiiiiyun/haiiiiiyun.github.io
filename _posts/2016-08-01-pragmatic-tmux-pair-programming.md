---
title: Tmux 学习摘要5--结对编程
date: 2016-08-01
writing-time: 2016-08-01 22:57--00:00
categories: programming
tags: Tmux
---

使用 tmux 进行结对编程的两种方式：

1. 创建一个新帐户。在该新用户下创建 tmux 开发环境，其他组员和你共享这个新帐户，并在其下工作。
2. 使用 tmux 的 sockets，使得其他人能连接到你的 tmux 会话。

这两种方式本质上都有安全隐患：别人会看到你屏幕上的内容。因此，较好的方法是在 VPS 或虚拟机（VirtualBox + Vagrant）上搭建开发环境用于结对编程共享。

# 共享帐户下的结对编程

 这是一种最简单的方法。先在一台主机上开启 SSH 访问，然后在上面安装和配置 tmux，并且创建一个 tmux 会话。其他用户用相同的帐户 SSH 到该主机，并且关联到该 tmux 会话。举例来说，假设主机运行 Ubuntu，并且名称为 *puzzles*。

 首先，创建一个用于共享的帐户 **tmux** ：

 ```sh
 tmux@puzzles$ adduser tmux
 ```

 为使其他用户能通过 SSH 无缝地登录主机，在主机的 tmux 帐户下建立 authorized_keys 文件：

 ```sh
 tmux@puzzles$ su tmux
 tmux@puzzles$ mkdir ~/.ssh
 tmux@puzzles$ touch ~/.ssh/authorized_keys
 tmux@puzzles$ chmod 700 ~/.ssh
 tmux@puzzles$ chmod 600 ~/.ssh/authorized_keys
 ```

 然后，在客户机上，将自己的 *id_rsa.pub* 文件传送给主机：

 ```sh
 $ scp -p id_rsa.pub tmux@puzzles.local
 ```

 再回到主机，将开发人员的 key 添加到 *authorized_keys* 文件：

 ```sh
 tmux@puzzles$ cat id_rsa.pub >> ~/.ssh/authorized_keys
 ```

 重复这个流程，直到所有结对编程人员的 key 都已添加完毕。

 在主机上设置 tmux 开发环境，然后创建一个会话：

 ```sh
 tmux@puzzles$ tmux new-session -s Pairing
 ```

 然后团队中的任何一个成员都可以登录到主机，并且关联到该会话：

 ```sh
 tmux@puzzles$ tmux attach -t Pairing
 ```

 之后，团队就能在该项目上协作了。并且团队成员可以随时脱离这个会话，然后可以再关联回来。

# 使用共享帐户及分组会话

当两人同时关联到相同的会话时，他们会看到相同的内容，并且是和相同的窗口交互。但是允许互不干扰地在会话中操作有时会很有用。该功能可用 **分组会话** 实现。以例子说明：

先在远程主机上创建一个新的会话 *groupedsession* ：

```sh
tmux@puzzles$ tmux new-session -s groupedsession
```

之后，其它用户不是关联该会话，而是在创建他自己的会话时将该会话作为一个目标会话，从而 "加入" 到 groupedsession 会话：

```sh
 tmux@puzzles$ tmux new-session -t groupedsession -s mysession
```

当第二个会话加载后，此时每个用户都在与 groupedsession 会话交互，但是每个用户自己创建的窗口，虽然其他用户可以在状态栏中看到窗口名，但是不能操作，从而实现了会话的共享和操作的隔离。


# 使用独立帐户和 Socket 进行结对编程

通过使用 tmux 的 socket 功能，可以创建多人可连接的会话。

首先，为该会话创建两个新帐户，ted 和 barney：

```sh
tmux@puzzles$ sudo adduser ted
tmux@puzzles$ sudo adduser barney
```

然后，创建 "tmux" 组，并且创建 */var/tmux* 目录用于保存共享会话：

```sh
tmux@puzzles$ sudo addgroup tmux
tmux@puzzles$ sudo mkdir /var/tmux
tmux@puzzles$ sudo chgrp tmux /var/tmux
```

设置目录权限使得 tmux 组中的成员都能对其进行读写：

```sh
tmux@puzzles$ sudo chmod g+ws /var/tmux
```

将帐户添加到 tmux 组：

```sh
tmux@puzzles$ sudo usermod -aG tmux ted
tmux@puzzles$ sudo usermod -aG tmux barney
```

## 创建并共享会话

之前用 **new-session** 命令创建的会话使用了默认的 socket 地址，它们都无法访问到。现在 ted 用 `-S` 开关创建一个会话：

```sh
ted@puzzles$ tmux -S /var/tmux/pairing
```

在另一个终端中，以 barney 帐户登录，然后用 `-S` 开关来关联这个 socket 型的会话：

```sh
barney@puzzles$ tmux -S /var/tmux/pairing attach
```

这样， barney 和 ted 就关联到了同一个会话，并且可以看到相同的内容。

这种方式中，会话加载时使用的是创建该会话的帐户下的 *.tmux.conf* 文件。

# 总结

使用这些方法，可以在生产环境下的服务器上开启一个会话：开启监测工具等，然后脱离关联，之后再返回关联。或者可以在 VPS 上创建一个会话，并设置 好开发环境，之后，可以在任何地方，任何设备上返回关联这个会话，继续之前的工作。

## 命令

命令                                                 | 描述
-----------------------------------------------------|
tmux -S [socket]                                     | 使用 socket 创建一个会话
tmux -S [socket] attach                              | 使用 socket 关联一个会话
tmux new-session -t [existing-session] -s [newssion] | 连接到一个分组会话


参考资源：

[tmux: Productive Mouse-Free Development](https://pragprog.com/book/bhtmux/tmux)
