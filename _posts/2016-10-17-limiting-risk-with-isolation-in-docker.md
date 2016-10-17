---
title: Docker 中通过隔离来限制风险
date: 2016-10-17
writing-time: 2016-10-17 09:59
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 资源限制

## 内存限制

它限制容器中的进程可以使用的内存量。可以通过在 `docker run` 或 `docker create` 中加 `-m` 或 `--memory`选项来实现限制，该选项接受一个值和单位，格式如下：

`<number><可选的一个单位> 其中单位=b(指byte), k(指kb), m(指mb) 或 g(指gb)`

开启一个最好能使用 256m 内存的数据库容器：

```bash
$ docker run -d --name ch6_mariadb \
    --memory 256m \
    --cup-shares 1024 \
    --user nobody \
    --cap-drop all \
    dockerfile/mariadb
```

这里只是限制为最多能使用 256m，并不是表示为该容器保留 256m 内存。在一个有 swap 的系统上，容器限制的内存甚至可以超过主机的物理内存。


## CPU 限制

有两种方法，一种是通过在 `docker run` 或 `docker create` 中的 `--cpu-shares` 选项为容器提供一个相对的权重，如：

```bash
$ docker run -d -P --name ch6_wordpress
    --memory 512m \
    --cpu-shared 512 \
    --user nobody \
    --cap-drp net_raw \
    --link ch6_raw \
    wordpress:4.1
```

上面开启的 MariaDB 容器的相对 CPU 权重是 1024，而 WordPress 的为 512，应该 MariaDB 容器获取的 CPU 周期数为 WordPress 的两倍。如果再开一个权重为 2048 的容器，那么总权重份数为 1024+512+2048，而第三个容器获取的 CPU 周期数约占 2048/(1024+512+2048)=0.57。

![相对权重与 CPU 共享数](/assets/images/dockinaction/docker-relative-weight-and-cpu-shares.png)

另一种方法是通过在 `docker run` 或 `docker create` 中的 `--cpuset-cpus` 选项将容器限制在某些核上运行。

在多核机器上，防止多个容器在相同核上运行，能最大化多核的使用。

```bash
# 将容器限制运行在编号为 0 的核上
$ docker run -d \
    --cpuset-cpus 0 \
    --name ch6_stresser dockerinaction/ch6_stresser

# 开启另一个容器来显示机器上 CPU 的负荷
$ docker run -it --rm dockerinaction/ch6_htop
```

`--cpuset-cpus` 的值可以为：

+ 单个 CPU 编号， 如 `0`
+ 以 `,` 分隔的多个 CPU 编号，如 `0,1,2`
+ 以 `-` 连接的 CPU 编号区间，如 `0-2`


## 限制对设备的访问

通过 `--device` 将主机上的设备挂载到容器中，如将主机上的摄像头设备挂载到容器中的相同位置：

```bash
$ docker -it --rm \
    --device /dev/video0:/dev/vide0 \  # mount video0
    ubuntu:latest ls -al /dev
```

该选项可以使用多次来将多个设备挂载到容器中，格式为 `--device dev_path_on_host:dev_path_on_container`。


# 内存共享

这种类型的 IPC 性能好于基于网络或管道的 IPC。

## 在容器间共享 IPC 原语

dockerinaction/ch6_ipc 映像内包含有一个 producer 和 consumer，它们通过共享内存通信。producer 创建一个消息队列，并把消息广播到队列中，而 consumer 会从队列中提取消息并写入日志。开启两个容器并查看日志：

```bash
$ docker run -d -u nobody --name ch6_ipc_producer \
    dockerinaction/ch6_ipc -producer

$ docker run -d -u nobody --name ch6_ipc_consumer \
    dockerinaction/ch6_ipc -consumer

$ docker logs ch6_ipc_producer
$ docker logs ch6_ipc_consumer
```

上面的例子中，会出现 ch6_ipc_consumer 中没有任何日志，这是因为虽然这两个容器中的进程都引用了相同的共享内存资源，但是由于每个容器都有各自独立的共享内存命名空间，因此引用的是完全不同的内存。

如果共基于共享内存通信，通信的容器必须通过 `--ipc` 选项将 IPC 命名空间组合起来，这种 `--net` 选项是类似的：

```bash
$ docker rm -v ch6_ipc_consumer # remove original consumer
$ docker run -d --name ch6_ipc_consumer \
    --ipc container:ch6_ipc_producer \ # join IPC namespace
    dockerinaction/ch6_ipc -consumer 

$ docker logs ch6_ipc_producer
$ docker logs ch6_ipc_consumer
```

## 使用开放内存容器 (open memory container)

开放内存容器相互之间，以及与主机之间都能进行内存共享。它通过 `--ipc host` 实现：

```bash
$ docker run -d -u nobody --name ch6_ipc_producer \
    --ipc host \
    dockerinaction/ch6_ipc -producer

$ docker run -d -u nobody --name ch6_ipc_consumer \
    --ipc host \
    dockerinaction/ch6_ipc -consumer

$ docker rm -vf ch6_ipc_producer ch6_ipc_consumer
```

应尽量少用这种类型的容器。


# 理解系统用户

在容器中 Docker 默认使用的是 root 用户。

## Linux USR 命名空间简介

Linux 最新的 user(USR) 命名空间允许将一个空间中的用户映射到另一个空间中，它和 PID 命名空间类似。

但是 Docker 还没有整合 USR 命名空间。因此容器中用户和主机上的用户，只要 user ID 相同，那么在容器和主机上都具有相同的权限。故容器中的高权限用户通过 Volume 会影响主机上的文件系统。


待续。。。











参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Limiting risk with isolation](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
