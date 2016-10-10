---
title: 使用 Docker 简化软件的安装
date: 2016-10-10
writing-time: 2016-10-10 10:57--14:48
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

Docker 将软件安装工作分成了三步：

1. 如何标识软件？
2. 去何处查找要安装的软件？
3. 都安装了哪些文件以及如何进行隔离？

用 Docker 发布的软件都是映像文件形式，可以用 repository 和 tag 来标识。

# 标识（命名）软件 

我们知道 Docker 容器创建自映像文件。映像文件包含有：

+ 创建自它的容器可用的数据文件
+ 元数据：有关各映像文件间的相互关系、该映像的命令历史、导出的端口、Volumes 定义等


映像文件都有一个很长的标识号，并且当映像文件每次修改后，该标识号也会跟着改变，因此不宜用它来标识软件。

## 用仓库 (repository) 来标识软件

映像的仓库名类似于 URL，比如 `quay.io/dockerinaction/ch3_hello_registry`，它的组成：

+ 存储映像的主机名，如 `quay.io`
+ 映像的所有者账号，如 `dockerinaction`
+ 映像的短名字，如 `ch3_hello_registry`


## 用标签 （tag) 来标识软件版本

一个仓库可保存一个映像的多个标签（Tag），即相对于一个软件的多个版本，一个标签对应一个版本。rep:tag 可唯一标识一个软件。

当没有指定 tag 时，默认的 tag 值为 latest。

# 查找和安装软件

默认的软件注册中心是 Docker Hub，如果没有指定其它的注册中心，使用 `docker pull` 或 `docker run` 会默认到 Docker Hub 上查找资源。


## 用命令行访问 Docker Hub

+ `docker login` 登录 Docker Hub。
+ `docker logout` 退出。
+ `docker search` 搜索软件，如 `docker search postgres`。
+ `docker pull` 下载软件。

映像 `docker push` 到 Docker Hub 有两种方法：

+ 自己在本地系统上创建映像文件并上传，这样上传的映像可信值不高，因为可能会包含恶意代码
+ 发布一个 Dockerfile，上传后由 Docker Hub 的持续构建系统自动构建，这种的可信值较高


## 访问 Docker Hub 网站

地址： [hub.docer.com](https://hub.docer.com)


Docker Hub 不可能是唯一的软件源。

安装 Docker 的其它方法有：

+ 使用其它的注册中心或自己的注册中心
+ 手动从一个文件导入映像
+ 根据下载项目中的 Dockerfile 文件自己构建一个映像


## 使用其它的注册中心

只需写全映像仓库名即可，如：

```bash
$ docker pull quay.io/dockerinaction/ch3_hello_registry:latest
```

仓库地址的完整格式为： `[RegistryHost/][Username/]Name[:Tag]`

这种方式安装后，删除映像也要用完整的仓库名：

```bash
$ docker rmi quay.io/dockerinaction/ch3_hello_registry
```


## 从文件导入映像

```bash
$ docker pull busybox:latest # 先下载 busybox 映像

$ docker images # 会看到 busybox 映像

$ docker save -o myfile.tar busybox:latest # 将映像保存为一个文件

$ docker rmi busybox
$ docker images # 现在已经删除了 busybox 映像

$ docker load -i myfile.tar
$ docker images # 又可以看到 busybox 映像
```

`save` 命令的 `-o` 参数指定保存的文件名，由于该命令的格式为 tar, 故用 .tar 后缀。很多程序都用 tar 格式来打包数据，但用不同的后缀，如 .jar, .war, .ear 等。


## 从 Dockerfile 文件安装

Dockerfile 文件是一个脚本，里面包含构建一个映像的所有步骤。一般将 Dockerfile 通过源码发布，然后用 `docker build` 命令构建映像：

```bash
$ git clone https://github.com/dockerinaction/ch3_dockerfile.git
$ docker build -t dia_ch3/dockerfile:latest ch3_dockerfile
```

上面的 `-t` 选项指定构建出的映像的仓库名。

这种安装方式的缺点有：

+ 构建过程花费时间
+ 构建中使用的一些依赖数据可能会找不到


因此这种方式不适合于为用户发布软件。


# 安装的文件及隔离性

## Image  layers

一个映像(image) 实际上是一组映像层 (image layers)。映像中的各层相互叠加，相互依赖。

一个映像一般由一个基础映像层（如 ubuntn:latest）加上自定义层组成。

## 容器文件系统抽象和隔离性

容器内的程序无需了解映像层的信息。在容器看来，这些自映像中复制过来的文件都是独立的，不会和其它容器混淆。

Docker 通过 UFS（union file system) 、MNT (mount) 命名空间和 chroot 系统调用来实现文件系统的隔离性。

UFS 在主机文件系统上创建挂载点，以对层的使用进行抽象。这些创建的层就是绑定在 Docker 映像中的层。类似地，当 Docker 映像安装后，它里面的层会被拆解出来。之后 UFS 会根据主机的情况选择采用一种具体的文件系统方案，为这些层进行适当的配置。

Linux 内核提供了 MNT 命名空间。当创建一个容器时，该容器将有一个自己的 MNT 命名空间，Docker 会为该容器创建一个新的挂载点。

最后，调用 `chroot` 为该容器设置一个文件系统 root。


## 分层结构的好处

映像由多个映像层组成，那么在下载安装时，一些基本映像可以共享，从而避免重复下载、存储和安装。

## UFS 的弱点

Docker 会基于运行的系统选择最适合的文件系统，但是不同的文件系统就文件属性、大小、名字、字符集等都会有区别。因此，在跨系统时可能会有问题。

可以使用 `docker info` 命令来查看 Docker 采用的是哪种文件系统。如何要指定 Docker 使用哪种文件系统，可在启动 Docker 后台程序时添加 `--storage-driver` 或 `-s` 选项。


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Software installation simplified](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
