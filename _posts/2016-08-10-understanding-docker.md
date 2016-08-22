---
title: 理解 Docker
date: 2016-08-10
writing-time: 2016-08-10 13:26--2016-08-22 11:25
categories: programming
tags: Docker
---

# 概述

Docker 是一个用于开发、部署和运行应用的开源平台。它意在使你能更快地进行应用分发。

使用 Docker 可以将应用系统和基础设施分离，并且可以用管理应用系统类似的方式对基础设施进行管理。

Docker 使用了内核的容器功能 + 工作流程 + 工具来助我们管理和部署应用。

# 什么是 Docker 平台

Docker 内核能将应用安全地运行于一个个容器中。同时，它的容器是轻量级的，因而可以在一台主机上同时运行很多个容器。

围绕容器还提供了相关的工具和平台：

+ 将应用（及其相关组件）放到一个 Docker 容器中
+ 将容器打包发送给团队成员进行再一步的开发和测试
+ 将应用部署到生产环境中，无论部署到本地还是云中


# 什么是 Docker 引擎

Docker 引擎是一个 CS 框架的应用程序，有下面几个主要组件：

+ 服务端 server 是一个一直在后台运行的进程
+ REST API 是客户端及其它程序与服务端交互的接口
+ 一个命令行客户端 CLI


![Docker 主要组件](https://docs.docker.com/engine/article-img/engine-components-flow.png)

CLI 以脚本或直接命令的形式，利用 Docker REST API 和 Docker 后台进程交互。而其它的 Docker 应用也会使用 REST API 和 CLI。

后台对 Docker 对象进行创建和管理。Docker 对象包括 images, containers, networks, data volumnes 等。

# Docker 的用途

## 更快分发

在本地，开发人员将应用代码和运行所需的相关服务一起放置在一个本地 Docker 容器中，并将其（包含代码及所有开发堆栈)发送给同事。开发完成后，他们可以将代码及开发堆栈推送到一个测试环境中进行测试。在测试环境中，又可以将 Docker images 推送到生产环境中进行部署。

## 更加容易部署和扩展

其基于轻量级容器的特性使得它非常容易进行扩展。 Docker 容器可以运行在开发者机器上，数据中心的物理或虚拟机上，或者云上。

由于容器与低层基础设施分离，可以实现实时的升配和降配。

## 实现高密度计算，承担更多负荷

性能上相比虚拟机高效地多。

# Docker 的体系结构

CS 框架。Docker 后台进程负责创建、运行和发布 Docker 容器。Docker 客户端和后台进程即可以运行在同一个机器上，也可以运行在不同的机器上。Docker 客户端通过 sockets 或 REST API 与后台进程通讯。

![Docker 体系结构](https://docs.docker.com/engine/article-img/architecture.svg)

## Docker 后台进行

运行于服务器上，用户通过 Docker 客户端与其交互。

# Docker 客户端

即二进制程序 **docker**，它接受用户命令，将命令传给 Docker 后台进程，然后将命令结果返回给用户。

## Docker 的内部机制

要理解 Docker 的内部机理，要知道三种资源：

+ Docker images
+ Docker registers
+ Docker containers


## Docker images (Docker 映像）

Docker image 是一个只读模板。例如，一个 Docker image 可以包含一个 Ubuntu 操作系统、Apache 及你安装的程序。Image 用来创建 Docker 容器。Docker 可以非常容易地创建新 image 或者更新现成的 image，或者你也可以下载别人制作的 image。

Docker image 是 Docker 的 **构建** 组件。

## Docker registries (Docker 登记中心）

Docker registries 保存 Docker images。它就是一个仓库，即有私有的也有公共的，可以从中上传或下载 images。公共 Docker registry 是 [Docker Hub](http://hub.docker.com/)。Docker registries 是 Docker 的 **分发** 组件。

## Docker containers (Docker 容器)

Docker 容器类似目录。一个容器包含所需运行程序的所有依赖。每个容器都根据一个 Docker image 创建。Docker 容器可以被运行、开启、停止、移动或者删除。每个容器都是一个隔离地安全的应用平台。Docker 容器是 Docker 的 **运行** 平台。

# Docker image 工作原理

每个 image 包含一系列的层。Docker 利用 [union file systems](http://en.wikipedia.org/wiki/UnionFS) 将这些层合并到一个 image 中。UnionFS 允许不同文件系统（被称作分支）的文件和目录进行透明的层叠，从而形成一个单一的一致的文件系统。

采用层是 Docker 轻量级的一个原因。例如，当你对应用进行了升级后，就会创建一个新的层，从而完成对 image 的修改。无需对整个 image 进行重建，只需添加或更新相关的层即可。在分发时，也只需分发更新了的层。

每个 image 都开始于一个最基本的 image ，如 *ubuntu*，然后在些基础上构建新的 image。

在基 image 之后，通过运行一组步骤（称为指令）来创建出新的 image。每个指令在我们的 image 上创建一个新的层。

指令动作包含：

+ 运行命令
+ 添加文件或目录
+ 创建环境变量
+ 加载容器时运行哪个进程


这些指令保存在 **Dockerfile** 文件中。**Dockerfile** 是一个脚本文件，包含了从基 image 创建所需 image 的所有指令和命令。


# Docker registry 工作原理

Docker registry 是 Docker images 的仓库。当创建了一个 Docker image 后，可以将它 **push** 到公共 registry 上如 Docker Hub 中。

通过 Docker 客户端，可以搜索已发布的 image, 然后将它 **pull** 到 Docker 主机上，最后根据它启动容器。

# 容器工作原理

一个容器包含一个操作系统，用户添加的文件及元数据。容器创建自一个 image。image 告诉 Docker 一个容器中都包含什么内容，当容器加载时要运行哪个进程，以及其它的配置数据。Docker image 是只读的。而当 Docker 根据一个 image 开启了一个容器后，它将在 image 之上添加一个读写层，而我们的应用就运行于其之上。


# 当运行一个容器时发生的事情

运行一个容器：

```shell
$ docker run -i -t ubuntu /bin/bash
```

上面的命令中：

+ 指定了从 **ubuntu** 这个 image 创建出一个窗口
+ 当加载容器后，在容器中运行 **/bin/bash**


运行该命令时 Docker 引擎依次执行了如下操作：

+ Pull ubuntu image: 如果该 image 没有在本地缓存，则从 Docker Hub 上 pull 下来
+ 创建一个新的容器
+ 分配文件系统并添加一个读写层。容器在该文件系统中创建，并将一个读写层添加到该 image 上
+ 分配网络/桥接接口：创建一个网络接口使得容器能与本地主机通讯
+ 设置 IP 地址：从池中查找并关联一个 IP 地址
+ 执行指定的进程：如 /bin/bash
+ 获取应用的输出。


# 低层技术

使用 Go 编写，并利用了以下几个内核功能。

## Namespaces

运行容器时，Docker 会为该容器创建一组 namespaces，从而容器中的每个部件都运行于独立的 namespace 中，互不干扰。

Linux 上的 Docker 引擎用到的 namespaces：

+ pid namespace: 进程隔离
+ net namespace: 管理网络接口
+ ipc namespace: 管理 IPC 资源访问
+ mnt namespace: 管理挂载点
+ uts namespace: 隔离内核及版本标识（UTS：Unix Timesharing System)


## Control Groups 或 cgroups

Docker 引擎利用它实现容器间的硬件资源共享，并设置限制和约束。例如限制某个容器的内存使用量。

## Union file systems

Docker 引擎可以使用几个 ufs 的变种，如 AUFS, btrfs, vfs 和 DeviceMapper。

## Container format

Docker 引擎将这些组件合并成一个封闭体叫一个 container format，默认的 container format 叫 libcontainer。


> 参考文献： [Undering docker](https://docs.docker.com/engine/understanding-docker/)
