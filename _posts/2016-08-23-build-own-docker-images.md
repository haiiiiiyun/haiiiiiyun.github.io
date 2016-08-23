---
title: 构建自己的 Docker 映像文件
date: 2016-08-23
writing-time: 2016-08-23 15:03--15:54
categories: programming
tags: Docker
---

# 列出主机上的映像文件

```shell
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              14.04               1d073211c498        3 days ago          187.9 MB
busybox             latest              2c5ac3f849df        5 days ago          1.113 MB
training/webapp     latest              54bb4e8718e8        5 months ago        348.7 MB
```

可以看到：

+ 每个映像所在的仓库名， 如 `ubuntu`
+ 每个映像的标签 Tag，如 14.04
+ 每个映像的 ID

要想查看映像中的数据信息，可使用 [dockviz tool](https://github.com/justone/dockviz) 或 [Image layers site](https://imagelayers.io/)。

每个映像仓库中会有多个变种映像，就如每个 git 仓库中会有多个分支一样。比如在 `ubuntu` 仓库中，会有 12.04, 12.10 等的变种，每个变种映像都有一有对应的标签。因此，可以通过 `rep:tag` 的形式准确引用一个映像，如 `ubuntu:14:04`。

当没有指定标签时，默认的标签是 latest，故引用 `ubuntu` 实际上是引用 `ubuntu:latest`。


# 获取一个映像

```shell
$ docker pull centos

Pulling repository centos
b7de3133ff98: Pulling dependent layers
5cc9e91966f7: Pulling fs layer
511136ea3c5a: Download complete
ef52fb1fe610: Download complete
. . .

Status: Downloaded newer image for centos
```

可以看到，映像中的每一层都被独立下载。

# 查找映像

## 在 [Docker Hub 网站](https://hub.docker.com/) 上查找，或者在命令行中查找：

```shell
$ docker search sinatra
NAME                                   DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
training/sinatra                       Sinatra training image                          0                    [OK]
marceldegraaf/sinatra                  Sinatra test app                                0
mattwarren/docker-sinatra-demo                                                         0                    [OK]
luisbebop/docker-sinatra-hello-world                                                   0                    [OK]
bmorearty/handson-sinatra              handson-ruby + Sinatra for Hands on with D...   0
subwiz/sinatra                                                                         0
bmorearty/sinatra                                                                      0
. . .
```

可以看到有两种类型的映像仓库名，一种是像 `ubuntu` 这样的，这些是 Docker 公司发行的映像仓库名，还有一些如 `training/sinatra` 的仓库名，它的构成中，前缀是用户名。


# 创建自己的映像

创建映像有两种方式：

1. 更新一个容器，然后提到成一个新的映像
2. 使用 Dockerfile 来指定创建一个映像所需的指令


## 更新并提交成一个映像

先找到一个基映像，如 `training/sinatra`，再运行容器：

```shell
$ docker run -t -i training/sinatra /bin/bash

root@0b2616b0e5a8:/#
```

记录下容器的 ID 号 `0b2616b0e5a8`，之后要用到。

在容器中执行一些更新操作，比较安装一些程序，更新系统等。

更新完成后使用 `exit` 退出容器。再使用 `docker commit` 命令提交生成一个新的映像：

```shell
$ docker commit -m "Added json gem" -a "Kate Smith" \
0b2616b0e5a8 ouruser/sinatra:v2

4f177bd27a9ff0f6dc2a830403925b5360bfe0b93d476f7fc3231110e7f71b1c
```

+ `-m` 指定提交的注释
+ `-a` 指定作者名
+ `0b2616b0e5a8` 是容器 ID
+ `ouruser/sinatra:v2` 是生成的新映像的名称


在指定的映像名 `ouruser/sinatra:v2` 中， `ouruser` 是 Docker Hub 等 Docker 注册中心的用户名，`sinatra` 是映像的仓库名， `v2` 是标签。

可以查看生成的映像：

```shell
$ docker images

REPOSITORY          TAG     IMAGE ID       CREATED       SIZE
training/sinatra    latest  5bc342fa0b91   10 hours ago  446.7 MB
ouruser/sinatra     v2      3c59e02ddd1a   10 hours ago  446.7 MB
ouruser/sinatra     latest  5db5f8471261   10 hours ago  446.7 MB
```

## 根据 Dockerfile 文件构建一个映像

`docker commit` 是扩展现有映像的一种便捷方式，但是这种方式不便在团队间共享映像。

可以使用 `docker build` 从头构建一个新的映像。

先创建一个 Dockerfile 文件：

```shell
$ mkdir sinatra
$ cd sinatra
$ touch Dockerfile
```

在 Dockerfile 文件中写入指令，每个指令都在映像上生成一个新的层：

```conf
# This is a comment
FROM ubuntu:14.04
MAINTAINER Kate Smith <ksmith@example.com>
RUN apt-get update && apt-get install -y ruby ruby-dev
RUN gem install sinatra
```

指令的格式为：

```conf
INSTRUCTION statement
```

+ FROM 指令指定映像的基映像，如 ubuntu:14.04
+ MAINTAINER 指令指定映像的作者
+ RUN 指令指定需要在映像中运行的命令


使用 `docker build` 构建映像：

```shell
$ docker build -t ouruser/sinatra:v2 .

Sending build context to Docker daemon 2.048 kB
Sending build context to Docker daemon
Step 1 : FROM ubuntu:14.04
 ---> e54ca5efa2e9
Step 2 : MAINTAINER Kate Smith <ksmith@example.com>
 ---> Using cache
 ---> 851baf55332b
Step 3 : RUN apt-get update && apt-get install -y ruby ruby-dev
 ---> Running in 3a2558904e9b
Selecting previously unselected package libasan0:amd64.
(Reading database ... 11518 files and directories currently installed.)
Preparing to unpack .../libasan0_4.8.2-19ubuntu1_amd64.deb ...
...
Installing RDoc documentation for sinatra-1.4.5...
 ---> 97feabe5d2ed
Removing intermediate container 6b81cb6313e5
Successfully built 97feabe5d2ed
```

+ `-t` 即 target - 指定构建后的映像的名称
+ `.` 指定 Dockerfile 所在的目录


Docker 限制每个映像最多有 127 层，因此，要尽量优化映像层数。

# 为映像设置标签

```shell
$ docker tag 5db5f8471261 ouruser/sinatra:devel
```

该命令格式 `docker tag image_id username/rep:tag`。

# 映像的摘要信息 Digest

使用 v2 或之后格式的映像都有摘要信息，可以使用 `--digests` 列出：

```shell
$ docker images --digests | head

REPOSITORY        TAG      DIGEST                                                                     IMAGE ID      CREATED       SIZE
ouruser/sinatra   latest   sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf    5db5f8471261  11 hours ago  446.7 MB
```

在使用 2.0 格式的注册中心时，push, pull, create, run, rmi 及 Dockerfile 中的 FROM 命令都可通过 digest 来引用映像。

# 将映像推送到 Docker Hub

```shell
$ docker push ouruser/sinatra

The push refers to a repository [ouruser/sinatra] (len: 1)
Sending image list
Pushing repository ouruser/sinatra (3 tags)
. . .
```

# 从主机上删除映像

```shell
$ docker rmi training/sinatra

Untagged: training/sinatra:latest
Deleted: 5bc342fa0b91cabf65246837015197eecfa24b2213ed6a51a8974ae250fedd8d
Deleted: ed0fffdcdae5eb2c3a55549857a8be7fc8bc4241fb19ad714364cbfd7a56b22f
Deleted: 5c58979d73ae448df5af1d8142436d81116187a7633082650549c52c3a2418f0
```

> 参考文献： 
> [Docker docs: Build your own images](https://docs.docker.com/engine/tutorials/dockerimages/)
