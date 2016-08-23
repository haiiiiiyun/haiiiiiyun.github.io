---
title: 在 Docker 容器中运行 Hello world
date: 2016-08-23
writing-time: 2016-08-23 12:21--13:02
categories: programming
tags: Docker
---

#  运行 Hello world

```shell
$ docker run ubuntu /bin/echo 'Hello world'

Hello world
```

在本例中：

+ `docker run` 启动一个容器
+ `ubuntu` 是要运行的映像
+ `/bin/echo` 是要在容器中运行的命令


容器启动后，Docker 创建一个新的 Ubuntu 环境然后在容器内执行 `/bin/echo` 命令。

容器只有当你所指定的命令还在运行时才会保持运行。因此，在本例中，当 `/bin/echo` 命令执行完退出时，容器也一并退出。

# 开启一个交互式的容器

```shell
$ docker -t -i ubuntu /bin/bash

root@af8bae53bdd3:/#
```

本例中：

+ `-t` 选项在该容器中分配了一个仿真 tty/终端
+ `-i` 选项使我们能创建一个交互式的连接，从而能获取容器标准输入中的内容


输入 `exit` 或 `Ctrl-D` 退出交互式 shell ，同时容器也一并退出。

# 开启一个守护型的 Hello world

```shell
$ docker run -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"

1e5535038e285177d5214659a068137486f96ee5c2e85a4ac52dc83f2ebe4147
```

在本例中：

+ `-d` 选项使得容器在后台运行


`/bin/sh -c "while true; do echo hello world; sleep 1; done"` 是指定要运行的命令。而返回的一长串字符串是容器的 ID。我们之后可以通过容器 ID 或容器名字来访问该容器。

首先，用 `docker ps` 命令查看本例中的容器是否正在运行：

```shell
$ docker ps

CONTAINER ID  IMAGE         COMMAND               CREATED        STATUS       PORTS NAMES
1e5535038e28  ubuntu  /bin/sh -c 'while tr  2 minutes ago  Up 1 minute        insane_babbage
```

可以看到一些很有用的信息：

+ `1e5535038e28` 是容器 ID 的缩写
+ 命令、状态、以及随机分配的一个名字 `insane_babbage`


通过 `docker logs` 命令可以查看守护型容器的输出内容：

```shell
$ docker logs insane_babbage

hello world
hello world
hello world
. . .
```

通过 `docker stop` 命令可以关闭我们的守护型容器：

```shell
$ docker stop insane_babbage

insane_babbage
```

该命令会通知 Docker 优雅地关闭该容器，然后返回已关闭容器的名字。


# 总结

+ `docker ps` - 列出当前的活跃容器
+ `docker logs` - 显示容器标准输出上的内容
+ `docker stop` - 关闭容器


> 参考文献： 
> [Docker docs: Hello world in a container](https://docs.docker.com/engine/tutorials/dockerizing/)
