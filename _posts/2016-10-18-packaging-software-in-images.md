---
title: 使用 Docker 将软件打包成映像文件
date: 2016-10-18
writing-time: 2016-10-18 10:20
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 据容器构建 Docker 映像

## 打包一个 Hello World 映像

基本流程有 3 个步骤：

1. 先从某个现有映像创建一个容器
2. 在容器内的文件系统做修改（如安装、删除程序、创建文件等），这些修改会被写入容器的 UFS 上的新层中。
3. 最后提交这些修改。之后可据新创建的映像开启新的容器了。

举例如下：

```bash
$ docker run --name hw_container \
    ubuntu:latest \
    touch /HelloWorld  # modify file in container

$ docker commit hw_container hw_image # commit change to a new image

$ docker rm -vf hw_container # remove changed container

$ docker run --rm \
    hw_image \
    ls -l /HelloWorld  # examine file in new container

-rw-r--r-- 1 root root 0 Oct 18 07:43 /HelloWorld
```

## 打包一个含 Git 工具集的映像

### 先在容器中安装 git

```bash
$ docker run -it --name image-dev \
    ubuntu:latest /bin/bash # 开启一个交互的容器
$ apt-get update && apt-get -y install git  # 安装 git 及其依赖包
$ git version

git version 2.7.4
$ exit # 退出容器
```

### 检查文件系统的修改情况

`docker diff` 命令能将容器中的文件系统的所有修改情况列出，修改情况包括对文件和目录的添加(A)、修改(C)、和删除(D)。

```bash
$ docker diff image-dev  # a LONG list of file changes

```


### 提交成一个新的映像

使用 `docker commit` 来提交，它有几个选项：

+ `-a`: 作者名
+ `-m`: 提交消息


现将 image-dev 容器提交为 ubuntu-git 映像：

```bash
$ docker commit -a "@dockerinaction" -m "Added git" \
    image-dev ubuntu-git

sha256:d0746c6d107ba79a5453571672a9a04734e9bd4047a0daf65b52fca606453c47

$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu-git          latest              d0746c6d107b        39 seconds ago      254.5 MB

# 检验该映像是否含有 git 
$ docker run --rm ubuntu-git git version

git version 2.7.4
```

### 设置一个 entrypoint 再提交成新的映像

```bash
$ docker run --name cmd-git --entrypoint git ubuntu-git # show git help and exit
usage: git [--version] [--help] [-C <path>] [-c name=value]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           ...

$ docker commit -m "Set CMD git" \
    -a "@dockerinaction" cmd-git ubuntu-git # commit new image to same name

$ docker rm -vf cmd-git # cleanup
$ docker run --name cmd-git ubuntu-git version # since entrypoint is git, will exec `git version`
git version 2.7.4
```

将某个启动命令设置为 entrypoint, 能方便用户使用该映像。

## 配置映像的属性

当使用 `docker commit` 时，实际会提交一个新层到映像文件中。该次提交中不只包含有文件系统的快照，每层还会包含有描述执行上下文的元数据。

映像的以下信息在创建容器时会传递给容器：

+ 所有的环境变量
+ 工作目录
+ 设置的需暴露的网络端口
+ 所有的 Volume 定义
+ 容器的 entrypoint
+ 命令和参数


这些值如果没有指定，会比更早的基映像中继承。

举例：

```bash
$ docker run --name rich-image-example \
    -e ENV_EXAMPLE1=Rich -e ENV_EXAMPLE2=Example \
    busybox:latest # create env variable specialization

$ docker commit rich-image-example rie # commit image
$ docker run --rm rie \
    /bin/sh -c "echo \$ENV_EXAMPLE1 \$ENV_EXAMPLE2"

Rich Example

# 再添加新层
$ docker run --name rich-image-example-2 \
    --entrypoint "/bin/sh" \  # set default entrypoint
    rie \
    -c "echo \$ENV_EXAMPLE1 \$ENV_EXAMPLE2" # set default command

$ docker commit rich-image-example-2 rie #commit image
$ docker run --rm rie # different command with same output

Rich Example
```

# 深入理解 Docker 映像和层

续...


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Packaging Software in images](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
