---
title: 使用 Docker 将软件打包成映像文件
date: 2016-10-18
writing-time: 2016-10-18 10:20--2016-10-20 12:58
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 据容器构建 Docker 映像

## 打包一个 Hello World 映像

基本流程有 3 个步骤：

1. 先从某个现有映像创建一个容器
2. 在容器内的文件系统上做修改（如安装、删除程序、创建文件等），这些修改会被写入容器的 UFS 上的新层中。
3. 最后提交这些修改。之后可据新创建的映像开启新的容器。

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

`docker diff` 命令能列出容器中的文件系统的所有修改情况，修改情况包括对文件和目录的添加(A)、修改(C)、和删除(D)操作。

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

当使用 `docker commit` 时，实际会创建一个新层到映像文件中。该次提交中不只包含有文件系统的快照，每层还会包含有描述执行上下文的元数据。

映像的以下信息在创建容器时会传递给容器：

+ 所有的环境变量
+ 工作目录
+ 设置的需暴露的网络端口
+ 所有的 Volume 定义
+ 容器的 entrypoint
+ 命令和参数


这些值如果没有指定，会从更早的基映像中继承。

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

## 研究 UFS (union file system)

理解 UFS 的细节对于映像的制作者很重要：

+ 他们需要知道添加、修改、删除文件对最终映像的影响
+ 他们需要理解层之前的联系、以及层与映像、仓库和标签的联系


### 在 UFS 上添加文件

假设要在基映像 ubuntu 上新建一个文件，如下：

```bash
$ docker run --name mod_ubuntu ubuntu:latest touch /mychange
```

创建的容器将会停止，但 /mychange 文件会被写入到它自己的文件系统。容器的根文件系统是由它的映像提供的，并采用 UFS 实现。

UFS 由层构成。每次对 UFS 进行修改时，会在所有现有层之上创建一个新层，再在该新层上记录这些修改。

当从 UFS 上读取文件中，如果该文件存在于最上层，那么直接从最上层读取。如果该文件没有在最上层创建或修改过，那么读取操作会向下贯空各层，直到找到存在该文件的层。

层的这些功能已被 UFS 隐藏，容器中的进程无需了解这些细节。

### 在 UFS 上修改和删除文件

和添加操作类似，也是在最上层操作。删除文件时，会在最上层记录删除操作，这将隐藏下层的该文件。当修改文件时，修改也记录在最上层，它也会隐藏下层的该文件。对容器文件系统的修改列表可以通过 `docker diff container_name` 看到。

大多数 UFS 使用 copy-on-write 技术（可以理解为 copy-on-change)。当要对只读层（非最上层）上的文件进行修改时，在修改前，该文件先是从只读层被复制到可写层（最上层），然后在最上层记录修改。但这种方式对运行性能和映像文件的大小会有影响。

## 重新认识映像 images，层 layers，库 repositories， 和标签 tags

UFS 由层的堆栈组成。各层单独存储，它保存了对该层的一组修改记录及该层的元数据。当将容器的修改进行提交时，在容器的最上层中，会先生成一个 ID，再将要修改的原文件复制过来，最后将该层保存起来。该层的元数据包括：

+ 生成的层 ID
+ 该层的下层（父）的 ID
+ 创建该层的容器的运行上下文


层 ID 和元数据形成了一个图，而 Docker 和 UFS 据此图构建映像。

映像也是层的堆栈，可以从最上层开始，根据每层的元数据中的父 ID，按些链接依次访问到各层。而最上层的层 ID 实际也就是该映像的 ID。

映像 ID 也是 1024 位的十六进制编码字符串，不好记忆，可以通过 `docker tag`，`docker commit`，`docker build` 来制作标签。

如将一个容器提交成一个库和标签：

```bash
$ docker commit container_name myaccount/myfirstrepo:mytag
```

以上列出的 ID 会和 mod_ubuntu 不一样，因为已经创建了一个新层。

如果想复制一个映像，只需为一个现有库制作一个标签，可以用 `docker tag` ：

```bash
$ docker tag myaccount/myfirstrepo:mytag myaccount/new_image
```

它实际是复制了该映像，两个映像的 ID 是一样的。

容器中，除了最上层，其它层都是只读的，这种特性有助于基映像的共享，相同的基映像内容无需在不同的容器中多次复制。

## 管理映像的大小和层数

每次提交，都会创建新层，因此映像的大小是所有层的总和，肯定会越来越大。要列出映像中的所有层信息，用 `docker history` 命令，如： `docker history ubuntu-git:latest`。

像 git 中的 rebase 一样，可以将多个有抵消作用的层合并，从而可以减少映像的大小和层数。但如果用户已经下载了旧层，合并后会有问题。因此最好是为新映像创建分支。

# 导出和导入容器的文件系统

`docker export` 命令将容器中的整个 UFS 导出为一个文件，格式为 tarball，默认输出到标准输出。

例如：

```bash
$ docker run --name export-test \
    dockerinaction/ch7_packed:latest ./echo For Export

$ docker export --output contents.tar export-test
$ docker rm export-test
$ tar -tf contents.tar # show archive contents
```

而 `docker image` 命令会将一个 `tarball` 文件的内容全部导入到一个新映像中，它能识别多种压缩和未压缩的 tarball 格式。而在导入过程中，还可以加入可选的 Dockerfile 指令。导入文件系统是使映像保持最小文件大小的最简单方法，因为我们可以控制映像中的文件系统的内容。


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Packaging Software in images](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
