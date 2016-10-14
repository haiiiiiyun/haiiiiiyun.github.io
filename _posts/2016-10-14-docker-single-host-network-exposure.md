---
title: 单个主机上的 Docker 网络功能
date: 2016-10-14
writing-time: 2016-10-14 08:36
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# Docker 容器的网络

Docker 有两种网络：单机虚拟网和多机网络。本地虚拟网络助恶提供容器的隔离性。多机虚拟网络提供了中继功能，从而使得参与主机上的任何容器都有一个可被路由到了 IP 地址。

## 本地 Docker 网络拓扑

Docker 使用低层操作系统的功能来创建一个特定具可定制的虚拟网络拓扑。该虚拟网络是在 Docker 安装的机器上有见，它连接参与组网的各个 Docker 容器，也与主机所在的网络联通。

当然，通过开启 Docker daemon 及各容器的命令，你也可以调整该网络的行为和结构。下图显示了两个容器连到该虚拟网络的情况：

![连接有两个容器的 Docker 默认本地网络拓扑](/assets/images/dockerinaction/docker-default-network.png)

每个容器除了有自己的私有 loopback 接口外，还有另一个以太网络接口，该接口与主机命名空间内的一个虚拟接口连接。两这个连接起来的网络接口使得主机上的网络堆栈和容器的网络堆栈有效地连接了起来。和家中的网络一样，每个容器也各自分配了一个唯一的私有 IP，并且该 IP 对于外部网络不可见。

每个容器的虚拟接口都与 Docker 桥接接口 `docker0` 连接，从而这些容器形成了一个网络，而 `docker0` 最终与主机的网络相连。可以将 `docker0` 桥接接口想象成家里的路由器，容器中的所有联网都是通过 `docker0` 路由的。

使用 `docker` 命令定制所用的 IP 地址，`docker0` 所连接的主机网络接口，以及各容器的相互通信方式。各接口间的连接性描述了任何特定网络容器与网络其它部分的可见性和隔离性。Docker 利用内核的命名空间来创建这些私有虚拟接口，但是命名空间本身并不提供网络隔离性。网络的可见性和隔离性是通过主机的防火墙规则实现的。

## 网络容器(network container) 的 4 种原型

所有容器都属于这 4 种原型中的其中一个。这些原型定义了容器如何与本地的其它容器和主机网络交互。每种都有不同的目的，可以将每种都想象成不同级别的隔离性。创建容器时，要选用最强健（最佳隔离性）的原型。下图展示了这种原型的隔离性，左边的隔离性最强，右边的最弱：

![4 种容器网络原型及其与 Docker 网络的交互](/assets/images/dockerinaction/network-container-archetypes.png)

这两种网络原型为：

+ 关闭的容器 closed containers
+ 桥接容器 bridged containers
+ 组合容器 joined containers
+ 开放容器 open containers


# 关闭的容器 closed containers

这种容器没有网络连接，里面的进程只能使用 loopback 接口 （即可以使用 127.0.0.1 或 localhost)。

指定 `--net none` 可以创建这种原型的容器：

```bash
$ docker run --rm \
    --net none \
    alpine:latest \
    ip addr # only list the lo interface

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
```

```bash
$ docker run --rm 
    --net none \
    alpine:latest \
    ping -w 2 8.8.8.8 # ping google DNS is unreachable

PING 8.8.8.8 (8.8.8.8): 56 data bytes
ping: sendto: Network unreachable
```

这种原型最具隔离性，也最具安全性。适用于无需网络连接的任务。


# 桥接容器 bridged containers

这种原型的容器除了有一个私有的 loopback 接口，还有一个通过网桥连接到主机网络的私有接口。这种原型也最具可定制性。

所有连接到桥接虚拟接口 `docker0` 的网络接口都属于同一个虚拟子网。各子网内的容器可相互通信，同时，通过 `docker0` 也可以与主机的网络通信。

## 访问外网

选用桥接容器的最常见原因是其中的进程需要访问网络。如果不指定 `--net`，Docker 默认创建的就是格拉容器，当然也可以通过指定 `--net bridge` 来创建：

```bash
$ docker run --rm \
    --net bridge
    alpine:latest
    ip addr


1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
69: eth0@if70: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP 
    link/ether 02:42:c0:a8:00:02 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.2/20 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:c0ff:fea8:2/64 scope link tentative 
       valid_lft forever preferred_lft forever
```

可以看到，桥接的容器内有两个接口，一个 lo，另一个是以太接口。

## 定制名字解析

### 设定容器的 hostname

```bash
$ docker run --rm \
    --hostname barker \
    alpine:latest \
    nslookup barker

Name:      barker
Address 1: 192.168.0.2 barker
```

该命令设置了该容器的主机名 hostname，但是该 hostname 只能在该容器内可以解析。

### 设定 DNS 服务器

```bash
$ docker run --rm \
    --dns 8.8.8.8 \
    alpine:latest
    nslookup docker.com
```

这种方式使用创建的容器都使用固定的 DNS，确保了一致性。

注意事项：

+ 设置的值必须为 IP 地址。
+ `--dns=xxx` 可以设置多次，以设置多个 DNS 服务器
+ `--dns=xxx` 可以在启动 Docker daemon 时设置，这样该 Docker 启动的容器都有该 DNS 设置


### 设置 DNS 搜索的默认域名（默认主机后缀）

```bash
$ docker run --rm \
    --dns-search docker.com \
    busybox:latest \
    nslookup registry.hub
```

以上命令最终会对 `registry.hub.docer.com` 进行查询。

该特性常用来在内网中使用短名字，如访问内容的 wiki 可以为 `http://wiki/`。它还有更高级的用法：

假设有一台 DNS 服务器用于开发和测试，为避免硬编码环境相关的名字，如 `myservice.dev.mycompany.com`，可以这样使用：

```bash
$ docker run --rm \
    --dns-search dev.mycompany \
    busybox:latest \
    nslookup myservice  # 解析为 myservice.dev.mycompany

$ docker run --rm \
    --dns-search test.mycompany \
    busybox:latest \
    nslookup myservice  # 解析为 myservice.test.mycompany
```

使用这种模式，无需修改程序，只需指定运行的容器即可。

+ `--dns-search=xxx` 可以设置多次
+ `--dns-search=xxx` 可以在启动 Docker daemon 时设置，这样该 Docker 启动的容器都有该 DNS 设置

### 添加自定义的 "主机名<->IP" 映射

```bash
$ docker run --rm \
    --add-host test:10.10.10.255 \   # add host entry
    alpine:latest \
    nslookup test   # resolves to 10.10.10.255
```

该选项可以设置多次，但是和上面几个选项不同，它不能用于启动 Docker daemon。

所有这些添加的映像对实际上都保存在容器内的 `/etc/hosts` 文件中。

使用该功能，可以在容器中重定向某些主机。


## 开启入站通讯

桥接容器默认无法从主机外访问。但是可以通过端口映射将主机网络堆栈上的某个端口映射到容器中的某个端口，从而开启入站通讯。可以使用 `--publish=` 或 `-p` 来指定。

映像格式有 4 种形式：

+ `<containerPort>`: 将主机的所有接口上的某个动态端口绑定到容器中的该端口，如 `docker run -p 3333 ...`
+ `<hostPort>:<containerPort>`: 将主机的该端口绑定到容器中的端口，如 `docker run -p 3333:3333 ...`
+ `<ip>::<containerPort>`: 将主机上某 IP 地址的接口上的某个动态端口绑定到容器中的该端口，如 `docker run -p 192.168.0.32::2222 ...`
+ `<ip>:<hostPort>:<containerPort>`: 将主机上某 IP 地址的接口上的该端口绑定到容器中的端口上，如 `docker run -p 192.168.0.32:1111:1111 ...`


`-p` 选项可以使用多次来定义多个映射。













参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Network exposure](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
