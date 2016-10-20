---
title: Docker 中构建的自动化及高级映像
date: 2016-10-20
writing-time: 2016-10-20 14:00
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 通过 Dockerfile 打包 Git

先创建一个目录，在该目录中创建 Dockerfile 文件，内容如下：

```
# An example Dockerfile for installing Git on Ubuntu
FROM ubuntu:latest
MAINTAINER "dockerinaction@allingeek.com"
RUN apt-get update && apt-get install -y git
ENTRYPOINT ["git"]
```

在相同目录下，通过 `docker build` 来创建映像：

```bash
$ docker build --tag ubuntu-git:auto .

Successfully built 0bca8436849b
```

以上命令会生成一个 ubuntu-git:auto 映像。

Dockerfile 文件中的第一个命令必须为 `FROM`，用来指定基映像，如果没有基映像，可以指定为 `FROM scratch`。

`docker build` 命令的选项：

+ `--tag` 或 `-t` 指定生成的目标映像的名称和标签
+ `--file` 或 `-f` 指定 Dockerfile 文件的名称，如 BuildScript，该选项只指定了名称，文件的路径还是要由 `docker build` 的最后的位置参数确定


构建过程中每执行一步就会新增一个新层。这也意味着，构建过程会缓存各个步骤的结果，如果 Dockerfile 中的某个步骤出错了，下次重新构建时，会重用这些未出错的结果。如果不想用缓存，可以在 `docker build` 中加 `--no-cache`。

# Dockerfile 入门

## 元数据指令

本例子中先构建一个基映像，再根据该基映像构建两个新映像。

在构建过程中，通过 `.dockerignore` 文件指定在将文件从主机复制到映像的过程，忽略哪些文件。

`.dockerignore` 文件的内容可以如下：

```conf
.dockerignore
mailer-base.df
mailer-logging.df
mailer-live.df
```

创建基映像的 Dockerfile 文件 `mailer-base.df`：

```conf
FROM debian:wheezy
MAINTAINER Jeff Nickoloff "dia@allingeek.com"
RUN groupadd -r -g 2200 example && \
    useradd -rM -g example -u 2200 example
ENV APPROOT="/app" \
    APP="mailer.sh" \
    VERSION="0.6"
LABEL base.name="Mailer Archetype" \
    base.version="${VERSION}"
WORKDIR $APPROOT
ADD . $APPROOT
ENTRYPOINT ["/app/mailer.sh"]
EXPOSE 33333
# Do not set the default user in the base otherwise
# implementations will not be able to update the image
# USER example:example
```

运行以下命令来构建该其映像：

```bash
$ docker build -t dockerinaction/mailer-base:0.6 -f mailer-base.df
```

由于每执行 Dockerfile 中的一个命令，都会创建一个新的层，因此要尽可能地合并命令。

用到的几个新指令：

+ ENV，它可 `docker run` 和 `docker create` 命令中的 `--env` 选项功能一样，用来定义环境变量，定义后可在映像中使用，也可以在其它 Dockerfile 指令中引用，如本领中的 LABEL。
+ LABEL，它定义的键/值用于对映像或容器记录额外的无数据。它和 `docker run` 和 `docker create ` 命令中的 `--label` 选项功能一样。
+ WORKDIR，指定工作目录。
+ EXPOSE，指定要暴露的端口。
+ ENTRYPOINT，设置容器启动时要运行的程序。该指令有两种格式：shel 形式和 exec 形式。shell 形式的看起来像 shell 命令，并用空格分隔参数。而 exec 形式的是一个字符串数组，其中第一个值是要执行的命令，其它的都是参数。使用 shell 形式指定的命令将会被作为默认 shell 的参数运行，例如当指定 `ENTRYPOINT exec ./mailer.sh` 后，将会执行 `/bin/sh -c 'exec ./exec ./mailer.sh'`。更重要的是，如果 ENTRYPOINT 使用了 shell 形式，那么以后用 `CMD` 指令或在运行时通过 `docker run` 指定的额外参数都会被忽略掉，因此 shell 形式的 ENTRYPOINT 不灵活。

## 文件系统指令









参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Build automation and advanced image considerations](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
