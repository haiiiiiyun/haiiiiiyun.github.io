---
title: Docker Clusters、Machine 和 Swarm
date: 2016-12-21
writing-time: 2016-12-21 13:41
categories: programming Docker
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》 Cluster Swarm Docker&nbsp;Machine docker-machine
---

# Docker Machine 简介

通过 Docker Machine，可以将主机、云等基础设施抽象成一个个 Docker 虚拟机。

## 创建和管理 Docker Machine

Docker Machine 包含了许多的虚拟机驱动，如针对本地主机的 VirtualBox 等，在创建 Docker Machine 时，可根据选用的基础设施使用相应的驱动。

和 `docker-compose` 命令类似，针对 Docker Machine 的命令是 `docker-machine`。

### 安装 docker-compose

在 macOS 或 Linux 上：

```bash
$ curl -L https://github.com/docker/machine/releases/download/v0.8.2/docker-machine-`uname -s`-`uname -m` > docker-machine
$ sudo mv docker-machine /usr/local/bin/docker-machine && sudo chmod +x /usr/local/bin/docker-machine
```

```bash
$ docker-machine version
docker-machine version 0.8.2, build e18a919
```



通过 Docker Machine 在本地创建 3 个 Docker 虚拟主机：

```bash
$ docker-machine create --driver virtualbox host1
$ docker-machine create --driver virtualbox host2
$ docker-machine create --driver virtualbox host3
```

创建的 Docker 虚拟主机的信息都会保存在 `~/.docker/machine/` 下，内容包括与这些虚拟机建立安全通讯的认证信息、虚拟机使用的磁盘映像文件等。

```bash
$ docker-machine ls  # 列出所有管理的虚拟机
NAME    ACTIVE  DRIVER      STATE       URL                         SWARM
host1           virtualbox  Running     tcp://192.168.99.100:2376
host2           virtualbox  Running     tcp://192.168.99.101:2376
host3           virtualbox  Running     tcp://192.168.99.102:2376
```

ACTIVE 栏指出了当前活跃的虚拟机，所有通过 `docker` 和 `docker-compose` 发出的命令都与当前活跃的虚拟机交互。

```bash
$ docker-machine inspect host1  # 要查看虚拟机的详细信息

$ docker-machine inspect --format "{{.Driver.IPAddress}}" host1  # 获取其 IP
$ docker-machine ip host1  # 获取其 IP

$ docker-machine upgrade host3  # 升级虚拟机及其上面的软件

Stopping machine to do the upgrade...
Upgrading machine host3...
Downloading ...
Starting machine back up...
Starting VM...
```

docker-machine 的 inspect 命令和 docker 的 inspect 很相似，也都可以用 [Go 模板语法](http://golang.org/pkg/text/template/)。


### 与虚拟机的交互

当用 docker-machine 新建或登记一个虚拟机时，它会创建或导入一个 SSH private key 文件。`docker-machine ssh` 能根据这个 SSH private key 文件以授权用户登录虚拟机。

```bash
$ docker-machine ssh host1  # Bind your terminal to shell on host1
$ touch dog.file # create file on host1
$ exit # exit remote shell and stop command
```

如果只需执行命令，无需交互，也可以将要执行的命令作为 ssh 的参数：

```bash
$ docker-machine ssh host1 "echo spot > dog.file"
```

也可以通过 `scp` 在各虚拟机间进行文件传输：

```bash
$ docker-machine scp host1:dog.file host2:dog.file
$ docker-machine ssh host2 "cat dog.file" # -> spot
```

其它可用的命令举例：

```bash
$ docker-machine stop host2
$ docker-machine kill host3
$ docker-machine start host2
$ docker-machine rm host1 host2 host3
```







参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Clusters with Machine and Swarm](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
[Install Docker Machine](https://docs.docker.com/machine/install-machine/)
