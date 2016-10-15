---
title: 单个主机上的 Docker 网络功能
date: 2016-10-14
writing-time: 2016-10-14 08:36--2016-10-15 13:53
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# Docker 容器的网络

Docker 有两种网络：单机虚拟网和多机网络。本地虚拟网络有助于提高容器的隔离性。多机虚拟网络提供了中继功能，从而使得参与组网的任何主机上的任何容器都有一个可被路由到的 IP 地址。

## 本地 Docker 网络拓扑

Docker 使用低层操作系统的功能来创建一个可定制的虚拟网络拓扑。该虚拟网络只在 Docker 安装的机器上可见，它连接参与组网的各个 Docker 容器，也与主机所在的网络联通。

当然，通过开启 Docker daemon 及各容器的命令行，也可以调整该网络的行为和结构。下图显示了两个容器连到该虚拟网络的情况：

![连接有两个容器的 Docker 默认本地网络拓扑](/assets/images/dockerinaction/docker-default-network.png)

每个容器除了有自己的私有 loopback 接口外，还有另一个以太网络接口，该接口与主机命名空间内的一个虚拟接口连接。两这个相连的网络接口使得主机上的网络堆栈和容器的网络堆栈有效地连接了起来。和家中的网络一样，每个容器也各自分配了一个唯一的私有 IP，并且该 IP 对于外部网络是不可见。

每个容器的虚拟接口都与 Docker 桥接接口 `docker0` 连接，这些容器形成了一个网络，而 `docker0` 最终与主机的网络相连。可以将 `docker0` 桥接接口想象成家里的路由器，容器中的所有联网都是通过 `docker0` 路由的。

`docker` 命令可以定制所用的 IP 地址，`docker0` 所连接的主机网络接口，以及各容器的相互通信方式。各接口间的连接性描述了任何特定网络容器与网络其它部分的可见性和隔离性。Docker 利用内核的命名空间来创建这些私有虚拟接口，但是命名空间本身并不提供网络隔离性。网络的可见性和隔离性是通过主机的防火墙规则实现的。

## 网络容器(network container) 的 4 种原型

所有容器都属于这 4 种原型中的其中一种。这些原型定义了容器如何与本地的其它容器和主机网络交互的情况。每种都有不同的目的，都具有不同级别的隔离性。创建容器时，要选用最强健（最佳隔离性）的原型。下图展示了这种原型的隔离性，左边的隔离性最强，右边的最弱：

![4 种容器网络原型及其与 Docker 网络的交互](/assets/images/dockerinaction/network-container-archetypes.png)

这 4 种网络原型为：

+ 封闭的容器 closed containers
+ 桥接容器 bridged containers
+ 组合容器 joined containers
+ 开放容器 open containers


# 封闭的容器 closed containers

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

这种原型的容器除了有一个私有的 loopback 接口，还有一个通过网桥连接到主机网络的私有接口。这种原型最具可定制性。

所有连接到桥接虚拟接口 `docker0` 的网络接口都属于同一个虚拟子网。子网内的各容器可相互通信，同时，通过 `docker0` 也可以与主机的网络通信。

## 访问外网

选用桥接容器的最常见理由是其中的进程需要访问网络。如果不指定 `--net`，Docker 默认创建的就是桥接容器，当然也可以通过指定 `--net bridge` 来创建：

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

该命令设置了该容器的主机名为 hostname，但是该 hostname 只在该容器内可以解析。

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

以上命令最终会对 `registry.hub.docker.com` 进行查询。

该特性常用来在内网中使用短名字，如访问内容的 wiki 可以为 `http://wiki/`。它还有更高级的用法：

假设有台 DNS 服务器用于开发和测试，为避免硬编码环境相关的名称，如 `myservice.dev.mycompany.com`，可以这样使用：

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

该选项可以设置多次，但是和上面几个选项不同，它不能在启动 Docker daemon 时使用。

所有这些添加的映像对实际上都保存在容器的 `/etc/hosts` 文件中。

使用该功能，可以在容器中重定向某些主机。


## 开启入站通讯

桥接容器默认无法从主机外访问。但是可以通过端口映射将主机网络堆栈上的某个端口映射到容器中的某个端口，从而开启入站通讯。可以使用 `--publish=` 或 `-p` 来指定。

映身格式有 4 种：

+ `<containerPort>`: 将主机的所有接口上的某个动态端口绑定到容器中的该端口，如 `docker run -p 3333 ...`
+ `<hostPort>:<containerPort>`: 将主机的该端口绑定到容器中的端口，如 `docker run -p 3333:3333 ...`
+ `<ip>::<containerPort>`: 将主机上某 IP 地址的接口上的某个动态端口绑定到容器中的该端口，如 `docker run -p 192.168.0.32::2222 ...`
+ `<ip>:<hostPort>:<containerPort>`: 将主机上某 IP 地址的接口上的该端口绑定到容器中的端口上，如 `docker run -p 192.168.0.32:1111:1111 ...`


`-p` 选项可以使用多次来定义多个映射。

`-P` 或 `--publish-all` 选项会将映像中的所有标记为要暴露出来的端口全部与主机上的动态（临时）端口绑定。

因此，假设 ch5_expose 映像中标记了 5000、6000、7000 端口要暴露出来，那么下面的两条命令是等价的：

```bash
$ docker run -d --name dawson \
    -p 5000 \
    -p 6000 \
    -p 7000 \
    dockerinaction/ch5_expose

$ docker run -d --name woolery \
    -P \
    dockerinaction/ch5_expose
```

而在 `docker run` 中通过 `--expose port` 来指定需要暴露的端口，如：

```bash
$ docker run -d --name philbin \
    --expose 8000 \
    -P \
    dockerinaction/ch5_expose
```

要想查询具体的端口映射情况，可以用 `docker ps`, `docker inspect` 或 `docker port` 命令，如：

```bash
$ docker port philbin

5000/tcp -> 0.0.0.0:32771
6000/tcp -> 0.0.0.0:32770
7000/tcp -> 0.0.0.0:32769
8000/tcp -> 0.0.0.0:32768
```

## 容器间的通信 inter-container communication

所有本地桥接网络中的容器间默认都是联网的。要使这些容器间默认不能通信，在启动 Docker daemon 时要设置 `--icc` (inter-container commnication) 选项：

```bash
$ docker -d --icc=false ...
```

设置后，所有桥接网络中的容器间的通信默认都会被主机上的防火墙阻塞，只能通过添加显式的允许设置才能通信。

## 修改桥接网络的接口设置

### 设置网桥的地址及子网

在启动 Docker daemon 时，通过 `--bip` (bridge ip) 和 CIDR (classless inter-domain routing) 格式的地址来设置网桥 `docker0` 的 IP 地址和子网，假设要设置网桥的 IP 地址为 192.168.0.128，网络部分占用 25 位（那么主机部分只有 7 位）：

```bash
$ docker -d --bip "192.168.0.128"
```

设置后，该网络中可被分配的 IP 将为 192.168.0.128--192.168.0.255。网络设置好后，可以再设置容器可以被分配的 IP 地址段。假设在以上设置的网络中，先预留 192.168.0.128--192.168.0.192，只分配 192.168.0.192--192.168.0.255 的地址给容器：

```bash
$ docker -d --fixed-cidr "192.168.0.192/26"
```

### 设置网络的 mtu (包的最大字节数）

以内网的 mtu 为 1500 字节，设置举例：

```bash
$ docker -d -mtu 1200
```

### 设置定制的网桥

也可以通过 `-b` 或 `--bridge` ，使用自己的网桥接口来代替默认的 `docker0`:

```bash
$ docker -d -b mybridge ...

$ docker -d --bridge mybridge ...
```

# 组合的容器 Joined containers

创建新容器时，指定它与其它容器共享网络堆栈。

```bash
$ docker run -d --name brady \
    --net none alpine:latest \
    nc -l 127.0.0.1:3333

$ docker run -it \
    --net container:brady \
    alpine:latest netstat -al
```

上面例子中，brady 容器是一个 closed container 原型的容器，只有一个 lo 接口，而第二个容器指定与 brady 容器共享网络堆栈，因此它只能共用 brady 的 lo 接口。

由于共用网络堆栈，会出现端口、IP 绑定等冲突，都需要手动解决。

通过网桥连接的容器间的通讯是被主机上的防火墙规则限制的，而组合容器 (joined containers) 之间的通讯则不受限制。

## 何时使用

+ 当不同容器中的程序想通过一个 lo 接口进行通信时
+ 当一个容器中的程序修改网络堆栈，而另一个容器中的程序想使用这个修改过的网络堆栈时
+ 当想对另一个容器中的程序进行网络流量监测时


# 开放容器 Open Containers

它们能直接访问主机的网络，开放容器通过 `--net host` 创建：

```bash
$ docker run --rm \
    --net host \
    alpine:latest ip addr
```

上面的例子中，容器中的 `ip addr` 命令会列出主机上的所有网络接口的信息，包括接口 `docker0`。这种容器可以绑定 1024 以下的网络端口。

# 容器间的依赖关系

## 关联的本地服务发现功能

创建新容器时，可以指定关联其它正在运行的容器。在新建容器上关联其它容器时，会发生 3 件事：

+ 一个描述目标容器端点的环境变量会被创建
+ 目标容器的别名及其 IP 会在新建容器的 `/etc/hosts` 中创建
+ 假如容器间的通信被禁止的话，Docker 会特意为这两个关联的容器添加专门的防火墙规则。

但是容器间可访问的端口还是由目标容器定义的（如通过 `--expose` 选项指定）。

关联是本地运行时服务的一种更加静态的依赖关系。例如：

```bash
$ docker run -d --name importantData \ # named target of a link
    --expose 3306 \
    dockerinaction/mysql_noauth \
    service mysql_noauth start

$ docker run -d --name importantWebapp \ # create link and set alias to db
    --link importantData:db \
    dockerinaction/ch5_web startapp.sh -db tcp://db:3306

$ docker run -d --name buggyProgram \ # this container has no route to importantData, but it can access importantData through bridge interface
    dockerinaction/ch5_buggy
```

上面的例子中，如果容器间的通信没有被禁止，那么虽然 buggyProgram 容器没有关联到 importantData 容器，但它还是可以通过网桥来访问 importantData。


## 关联的别名

通过 `--link target_container:alias_name` 来关联，如：

```bash
$ docker run --link a:alias-a --link b:alias-b --link c:alias-c ...
```

但是当多个容器指定的别名一样时，会被覆盖，即 Docker 虽然会为每次别名定义添加防火墙规则，但是只会有一条起作用。

关联的别名作为容器要遵循别名的使用约定，例如一个容器中的程序可能会假设 `database` 别名存在，从而访问数据库时只需连接 `tcp://database:3306`; 或者容器中的程序也可能要通过环境变量 `DATABASE_PORT` 来查找连接信息。

问题是这种依赖没有一种好的定义及运行时检测机制。因此我们最好在容器的启动代码中添加依赖检测功能，例如 ch5_ff 的启动脚本中就包含这样的代码：

```bash
#!/bin/sh

if [ -z ${DATABASE_PORT+x} ]
then
    echo "Link alias 'database' was not set!"
    exit
else
    exec "$@"
fi
```

查看它的实效：

```bash
$ docker run -d --name mydb --expose 3306 \
    alpine:latest nc -l 0.0.0.0:3306 # create a link taget

$ docker run -it --rm \ # test without link
    dockerinaction/ch5_ff echo This "shouldn't" work.

Link alias 'database' was not set!

$ docker run -it --rm \
    --link mydb:wrongalias \
    dockerinaction/ch5_ff echo Wrong.

Link alias 'database' was not set!

$ docker run -it --rm \
    --link mydb:database \ # test correct alias
    dockerinaction/ch5_ff echo It worked.

It worked.

$ docker stop mydb && docker rm mydb
```

## 环境的修改

创建一个关联时会在新建的容器中添加连接信息。这些连接信息会通过在新建容器中添加一组环境变量及一个主机名映射来注入。

例如：

```bash
$ docker run -d --name mydb \
    --expose 2222 --expose 3333 --expose 4444/udp 
    alpine nc -l 0.0.0.0:2222

$ docker run -it --rm \
    --link mydb:database \
    dockerinaction/ch5_ff env

DATABASE_PORT_4444_UDP_ADDR=192.168.0.3
DATABASE_PORT_2222_TCP=tcp://192.168.0.3:2222
DATABASE_PORT_4444_UDP_PORT=4444
HOSTNAME=a4aa6e9c63ea
SHLVL=1
DATABASE_PORT_4444_UDP_PROTO=udp
HOME=/root
DATABASE_PORT=tcp://192.168.0.3:2222
DATABASE_PORT_3333_TCP=tcp://192.168.0.3:3333
DATABASE_NAME=/reverent_snyder/database
DATABASE_PORT_4444_UDP=udp://192.168.0.3:4444
TERM=xterm
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
DATABASE_PORT_2222_TCP_ADDR=192.168.0.3
PWD=/
DATABASE_PORT_2222_TCP_PORT=2222
DATABASE_PORT_3333_TCP_ADDR=192.168.0.3
DATABASE_PORT_2222_TCP_PROTO=tcp
DATABASE_PORT_3333_TCP_PORT=3333
DATABASE_PORT_3333_TCP_PROTO=tcp
```

可以看到，所有为该关联创建的环境变量都以该别名为前缀。同时，会有一个别名加 `_NAME` 为后缀的环境变量，它的值为当前容器名+关联的别名，如 `DATABASE_NAME=/reverent_snyder/database`。

对于关联中暴露的每个端口，会对应生成 4 个环境变量，模式如下：

+ `<ALIAS>_PORT_<PORT NUMBER>_<PROTOCOL TCP or UDP>_PORT`，如 `DATABASE_PORT_3333_TCP_PORT=3333`，它的值就是端口号，它可用于过滤如只含有 `TCP_PORT` 字符的环境变量列表。
+ `<ALIAS>_PORT_<PORT NUMBER>_<PROTOCOL TCP or UDP>_ADDR`， 如 `DATABASE_PORT_2222_TCP_ADDR=192.168.0.3`，它的值为关联容器的 IP 地址。
+ `<ALIAS>_PORT_<PORT NUMBER>_<PROTOCOL TCP or UDP>_PROTO`， 如 `DATABASE_PORT_2222_TCP_PROTO=tcp`。
+ `<ALIAS>_PORT_<PORT NUMBER>_<PROTOCOL TCP or UDP>`， 如 `DATABASE_PORT_3333_TCP=tcp://192.168.0.3:3333`。

还会创建一个额外的变量 `<ALIAS>_PORT`，它用来指向某个暴露的端口，如 `DATABASE_PORT=tcp://192.168.0.3:2222`。

## 关联的本质及其短板

关联的本质就是在创建新容器时，将已运行容器的连接信息（如 IP 地址，端口等）通过环境变量的方式注入到这个新建容器中。

因此，关联容器间的依赖关系是定向的、静态的、不可传递的。当被关联的容器 IP 地址发生改变时（如重启后），关联就会失效，因此，在这种情况时，不能通过关联来实现服务的发现，而应该通过 DNS 来实现。


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Network exposure](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
