---
title: Docker Clusters、Machine 和 Swarm
date: 2016-12-21
writing-time: 2016-12-21 13:41--2016-12-22 16:08
categories: programming Docker
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》 Cluster Swarm Docker&nbsp;Machine docker-machine
---

# Docker Machine 简介

通过 Docker Machine，可以将主机、云等基础设施抽象成一个个 Docker 虚拟机。

## 创建和管理 Docker 虚拟机

Docker Machine 包含了许多的虚拟机驱动，如针对本地主机的 VirtualBox 等，在创建 Docker Machine 时，可根据选用的基础设施使用相应的驱动。

和 `docker-compose` 命令类似，针对 Docker Machine 的命令是 `docker-machine`。

### 安装 docker-machine

在 macOS 或 Linux 上：

```bash
$ curl -L https://github.com/docker/machine/releases/download/v0.8.2/docker-machine-`uname -s`-`uname -m` > docker-machine
$ sudo mv docker-machine /usr/local/bin/docker-machine && sudo chmod +x /usr/local/bin/docker-machine

$ docker-machine version
docker-machine version 0.8.2, build e18a919
```


通过 Docker Machine 在本地创建 3 个 Docker 虚拟主机：

```bash
$ docker-machine create --driver virtualbox host1
Error with pre-create check: "VBoxManage not found. Make sure VirtualBox is installed and VBoxManage is in the path"
#Error with pre-create check: "This computer doesn't have VT-X/AMD-v enabled. Enabling it in the BIOS is mandatory"
# 如果没有 VirtualBox，会出现以上错误，需安装 VirtualBox:
$ sudo apt-get install virtualbox
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

ACTIVE 栏指出了当前活跃的虚拟机，所有通过 `docker` 和 `docker-compose` 发出的命令都只与当前活跃的虚拟机交互。

```bash
$ docker-machine inspect host1  # 查看虚拟机的详细信息

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

当用 docker-machine 新建或登记一个虚拟机时，它会创建或导入一个 SSH private key 文件。`docker-machine ssh` 能根据这个 SSH private key 文件授权用户登录虚拟机。

```bash
$ docker-machine ssh host1  # Bind your terminal to shell on host1
$ touch dog.file # create file on host1
$ exit # exit remote shell and stop command
```

如果只想执行命令，无需交互，可以将要执行的命令作为 ssh 的参数：

```bash
$ docker-machine ssh host1 "echo spot > dog.file"
```

也可以通过 `scp` 在各虚拟机间进行文件传输：

```bash
$ docker-machine scp host1:dog.file host2:dog.file
$ docker-machine ssh host2 "cat dog.file" # -> spot
```

其它可用的命令：

```bash
$ docker-machine stop host2
$ docker-machine kill host3
$ docker-machine start host2
$ docker-machine rm host1 host2 host3
```

## 配置客户端与远程的 docker daemon 交互

Docker Machine 用来管理 Docker 虚拟机。Docker Machine 管理的所有虚拟机中，任一时间最多只有一个是激活的，而与 `docker` 和 `docker-compose` 交互的就是这个已激活虚拟机中的 docker daemon （如果不是在 Docker Machine 环境中，交互的就是本机的 docker daemon）。

和 python virtualenv 类似，要想使用某个虚拟机，必须先激活该虚拟机并设置相关的环境。

先创建虚拟机：

```bash
$ docker-machine create --driver virtualbox machine1
$ docker-machine create --driver virtualbox machine2
```

`docker-machine env machine` 命令能根据用户本身的 shell 设置，导出虚拟机的相应环境设置命令，我们只需运行这些环境设置命令即可进入这个 virtualenv。

如果想为不同的 shell 导出环境设置命令，可添加 `--shell` 选项：

```bash
$ docker-machine env machine1 # let env autodetect your shell
$ docker-machine env --shell powershell machine1 # get PowerShell configuration
$ docker-machine env --shell cmd machine1 # get CMD configuration
$ docker-machine env --shell fish machine1 # get fish configuration
$ docekr-machine env --shell bash machine1 # get the default(POSIX) configuration
```

激活该虚拟机并进入环境：

```bash
$ eval "$(docker-machine env machine1)" # on POSIX shell
$ docker-machine env --shell=powershell machine1 | Invoke-Express # PowerShell on Win
```

可以通过 `active` 或 `ls` 子命令来验证哪个虚拟机被激活了：

```bash
$ docker-machine active  # or
$ docker-machine ls
```

激活后，所有的 docker 和 docker-compose 都将与该激活的虚拟机中的 docker daemon 交互，下面是使用举例：

```bash
$ docker pull dockerinaction/ch12_painted  # pull the image onto the active machine
$ eval "$(docker-machine env machine2)"
$ docker pull dockerinaction/ch12_painted  # pull  the image onto the active machine(machine2) again
```

可以看到，如果要对多个虚拟机进行相同的操作（如拉取相同的映像），需要针对不同的虚拟机进行多次相同的操作。

# Docker Swarm 简介

## 使用 Docker Machine 构建 Swarm cluster

一个 Swarm cluster 由两种机器组成。运行 Swarm 管理模式的机器叫管理器 manager，而运行 Swarm agent 的机器叫结点 node。而在其它所有方面，Swarm 管理器和结点没有任何区别，都是 Docker 虚拟机（每个虚拟机中都运行 Docker daemon）。

`docker-machine create` 命令可以用来创建 Swarm 机器，其有以下参数：

+ `--swarm`: 指明所创建的虚拟机将运行 Swarm agent 软件并加入一个 Swarm cluster
+ `--swarm-master`: 指明所创建的虚拟机将配置为 Swarm manager
+ `--swarm-discovery TOKEN_ID`: 指定需要加入或管理的 cluster TOKEN_ID


举例：

```bash
$ docker-machine create --driver virtualbox local # 创建一个普通的 Docker 虚拟机
$ eval "$(docker-machine env local)"  # 激活该虚拟机
$ docker run --rm swarm create  # 创建一个 Swarm Cluster, 将输出 Cluster TOKEN_ID
b26688613694dbc9680cd149d389e279

$ docker-machine create \  # 创建一个 Swarm manager 虚拟机
    --driver virtualbox \
    --swarm \
    --swarm-discovery token://b26688613694dbc9680cd149d389e279 \
    --swarm-master \
    machine0-manager

$ docker-machine create \ # 创建 Swarm 结点虚拟机
    --driver virtualbox \
    --swarm \
    --swarm-discovery token://b26688613694dbc9680cd149d389e279 \
    machine1


$ docker-machine create \ # 创建 Swarm 结点虚拟机
    --driver virtualbox \
    --swarm \
    --swarm-discovery token://b26688613694dbc9680cd149d389e279 \
    machine2

$ docker-machine ls  # 列出 Cluster 中的所有结点
NAME ...            URL                         SWARM
machine0-manager    tcp://192.168.99.106:2376   machine0-manager (manager)
machine1            tcp://192.168.99.107:2376   machine0-manager
machine2            tcp://192.168.99.108:2376   machine0-manager
```

## Swarm 扩展了 Docker Remote API

Swarm 的每个结点可以作为普通的 Docker 虚拟机使用，但是通过 Swarm manager，能将整个 Cluster 中的所有结点使用一个虚拟机使用。

要通过 Swarm manager 对 Cluster 进行管理，先激活 Swarm manager 虚拟机作为默认虚拟机：

```bash
$ eval "$(docker-machine env --swarm machine0-manager)" # or
$ docker-machine env --swarm machine0-manager | Invoke-Expression # PowerShell On Win
```

配置后， `docker` 命令接口就能使用 Swarm 的特有功能了，如 `docker info` 将列出整个 Cluster 的信息，而不只是某个 daemon的信息：

```bash
$ docker info

Containers: 4
Images: 3
Role: primary
Strategy: spread
Filters: affinity, health, constraint, port, dependency
Nodes: 3
  machine0-manager: 192.168.99.110:2376
    ? Containers: 2
    ? Reserved CPUs: 0 / 1
    ? Reserved Memory: 0 B / 1.022 GiB
    ? Labels: executiondriver=native-0.2, kernelversion=4.0.9-...
  machine1: 192.168.99.111:2376
    ? Containers: 1
    ? Reserved CPUs: 0 / 1
    ? Reserved Memory: 0 B / 1.022 GiB
    ? Labels: executiondriver=native-0.2, kernelversion=4.0.9-...
  machine2: 192.168.99.112:2376
    ? Containers: 1
    ? Reserved CPUs: 0 / 1
    ? Reserved Memory: 0 B / 1.022 GiB
    ? Labels: executiondriver=native-0.2, kernelversion=4.0.9-...
CPUs: 3
Total Memory: 3.065 GiB
Name: 942f56b2349a
```

在 Cluster 中创建一个容器：

```bash
$ docker run -t -d --name hello-swarm \
    dockerinaction/ch12_painted \
    Hello Swarm

# 由于是以后台方式运行的，结果会输出到日志中，故
$ docker logs hello-swarm


$ docker ps -a -f name=hello-swarm  # 过滤显示该容器在哪个 cluster 节点上运行

$ docker info # 可以看到现在多了一个容器和映像
Containers: 5 # swarm argent *3 + swarm manager + hello-swarm
Images: 4 # swarm 映像*3 + ch12_painted 映像


$ docker pull dockerinaction/ch12_painted # 将同时 pull 到 3 个 swarm 节点上
machine0-manager: Pulling dockerinaction/ch12_painted:latest... : downloaded
machine1: Pulling dockerinaction/ch12_painted:latest... : downloaded
machine2: Pulling dockerinaction/ch12_painted:latest... : downloaded

# 类似地，rm, rmi 等操作也会在所有的节点上进行相同的操作
```

# Swarm 调度

调度算法统筹容器在哪个结点上运行。共有 3 种调度算法， `spread` 是默认使用的算法，在 `docker-machine create` 时可以通过 `--swarm-strategy` 来指定采用哪种算法。

## Spread 算法

该算法会确保容器运行负荷在所有的结点上均匀分布。

举例，通过 `flock.yml` 定义 bird 服务：

```yaml
bird:
    image: dockerinaction/ch12_painted
    command: bird
    restart: always
```

开启 10 个容器，可以看到这些容器在结点上均匀分布：

```bash
$ docker-compose -f flock.yml scale bird=10  # create 10 birds

$ docker ps # checkout container distrubution

$ docker-compose -f flock.yml kill # clean up
$ docker-compose -f flock.yml rm -vf
```

这种算法适合如下情况：

+ 各容器的资源需求较均匀，差别不大


## 使用过滤器对调度进行调整

Swarm 调度器在应用任何调度算法前，会依据 Swarm 的配置及容器的需求先过滤候选的结点。

Cluster 中活跃的过滤器可以通过 `docker info` 看到，如：

```bash
$ docker info

Filters: affinity, health, constraint, port, dependency
```

各过滤器说明：

+ affinity: 与其它容器或映像的关系需求
+ constraint: 机器属性需求，如内核版本，存储，网速，磁盘类型等，也可以在创建结点时通过 `--engine-label` 在结点上应用 label 进行限制，如创建 label size=small, size=xxl 等，然后在创建容器时，通过注入环境变量来限制使用具有相应 label 的结点
+ dependency: link 或 共享 Volume 的依赖
+ port: 端口是否可用
+ health: 结点是否健康


例如：

```bash
$ docker-machine create -d virtualbox \
    --swarm \
    --swarm-discovery token://TOKEN_ID \
    --engine-label size=small \  # apply an engine label
    little-machine

$ docker-machine create -d virtualbox \
    --swarm \
    --swarm-discovery token://TOKEN_ID \
    --engine-label size=xxl \  # apply an engine label
    big-machine
```

除了 label, 容器可指定的限制有：

+ node: 结点的名字或 ID
+ storagedriver: 结点使用的存储驱动名
+ executiondriver: 结点使用的执行驱动名
+ kernelversion: 结点所在的 Linux 内核版本
+ operatingsystem: 结点所在的操作系统


容器通过环境变量来传递 affinity 和 constraint 需求，每个需求用一个环境变量实现，如：

```bash
$ docker run -d -e constraint:size=xxl \ # 环境变量以 constraint: 为前缀
    -m 4G \
    -c 512 \
    postgres


$ docker run -d -e affinity:image=nginx \ # 环境变量以 affinity: 为前缀，要求结点上已有 nginx 映像
    -p 80:80 nginx


$ docker run -d -e affinity:image!=nginx \ # 要求结点上没有 nginx 映像
    -p 8080:8080 haproxy

$ docker run -d -e affinity:image=~nginx \ # 只是建议结点上最好有 nginx 映像，如果实在没有也可以选用该结点
    -p 80:80 nginx
```

affinity 或 constraint 规则都由键，操作符和值组成，键必须是明确的值，值可以有如下格式：

+ 明确值，如 my-favorite.image-1
+ glob 语法的模式，如 my-favorite.image-*
+ Go 风格的正则表达式，如 `/my-[a-z]+\.image-[0-9]+/`


## 使用 BinPack 和 Random 进行调度

BinPack 算法趋向于先充分用完一个结节，然后再考虑下一个节点。而 Random 侧是随机选择结点。


# Swarm service discovery

## Swarm 和单机网络

在单机网络中，不同结点上的容器无法发现其它结点上的容器，因此关联的所有容器都将分布在同一个Cluster 虚拟机上。这是因为，即使使用了 Spread 调度算法，由于有 dependency 过滤器的作用，所有关联的容器只能选择同一个虚拟机。

## Ecosystem service discovery and stop-gap measures

网络服务发现功能主要是用 DNS 实现的。传统的 DNS 服务器大量依赖缓存，不适于高写入吞吐量的场景。而现代的系统，如 etcd, Consul, ZooKeeper, Serf 等都使用分布式的键值数据库、支持高写入吞吐量等，适合用于网络服务发现，但是将这些服务集成到容器中技术上有难度，同时也降低了容器应用的可移植性。

## 多机网络展望

理想的方案是通过 Docker Engine 和 Docker Swarm 将服务注册和发现功能集成到 Clustering 和网络层。

当前的实现版本通过 overlay 网络接口，将所有由 Docker Machine 管理并配置为使用同一个键值库的容器都处于同一个 overlay 网络中，相互可以路由到。



参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Clusters with Machine and Swarm](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
[Install Docker Machine](https://docs.docker.com/machine/install-machine/)
