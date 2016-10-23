---
title: 自动化构建 Docker 映像及高级映像
date: 2016-10-20
writing-time: 2016-10-20 14:00--2016-10-21 10:28
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

在相同目录下，通过 `docker build` 构建映像：

```bash
$ docker build --tag ubuntu-git:auto .

Successfully built 0bca8436849b
```

以上命令会生成一个 ubuntu-git:auto 映像。

Dockerfile 文件中的第一个命令必须为 `FROM`，它用来指定基映像，如果没有基映像，可以指定为 `FROM scratch`。

`docker build` 命令的选项：

+ `--tag` 或 `-t` 指定生成的目标映像的名称和标签
+ `--file` 或 `-f` 指定 Dockerfile 文件的名称，如 BuildScript，该选项只指定了名称，文件的路径还是要由 `docker build` 最后的位置参数确定


构建过程中每执行一步就会新增一层。构建过程会缓存各个步骤的结果，如果 Dockerfile 中的某个步骤出错了，下次重新构建时，会重用这些未出错的结果。如果不想用缓存，可在 `docker build` 中加 `--no-cache`。

# Dockerfile 入门

## 元数据指令

本例中先构建一个基映像，再根据该基映像构建两个新映像。

在构建过程中，通过 `.dockerignore` 文件指定在将文件从主机复制到映像的过程中，要忽略哪些文件。

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

由于每执行 Dockerfile 中的一个命令，都会创建一个新层，因此要尽可能地合并命令。

用到的几个新指令：

+ ENV，它与 `docker run` 和 `docker create` 命令中的 `--env` 选项功能一样，用来定义环境变量，定义后可在映像中使用，也可以在其它 Dockerfile 指令中引用，如本例中的 LABEL。
+ LABEL，它定义的键/值用于对映像或容器记录额外的元数据。它和 `docker run` 和 `docker create ` 命令中的 `--label` 选项功能一样。
+ WORKDIR，指定工作目录。
+ EXPOSE，指定要暴露的端口。
+ ENTRYPOINT，设置容器启动时要运行的程序。该指令有两种格式：shell 格式和 exec 格式。shell 格式的看起来像 shell 命令，并用空格分隔参数。而 exec 格式的是一个字符串数组，其中第一个值是要执行的命令，其它的都是参数。使用 shell 格式指定的命令将会被作为默认 shell 的参数运行，例如当指定 `ENTRYPOINT exec ./mailer.sh` 后，将会执行 `/bin/sh -c 'exec ./mailer.sh'`。更重要的是，如果 ENTRYPOINT 使用了 shell 格式，那么以后用 `CMD` 指令或在运行时通过 `docker run` 指定的额外参数都会被忽略掉，因此 shell 格式的 ENTRYPOINT 不灵活。

## 文件系统指令

Dockerfile 文件 mailer-logging.df 内容如下：

```conf
FROM dockerinaction/mailer-base:0.6
COPY ["./log-impl", "${APPROOT}"]
RUN chmod a+x ${APPROOT}/${APP} && \
    chown example:example /var/log
USER example:example
VOLUME ["/var/log"]
CMD ["/var/log/mailer.log"]
```

从上面的内容可看到，Dockefile 指令中可以使用基映像定义的环境变量，如 `APPROOT`。

+ COPY，该指令最少有两个参数，最后一个是目的文件/目录，其它的都是源文件。它有一个特性和我们预想的不一样：所有复制过来的文件的所有者都设为了 root，即使在 COPY 前设置了 USER 也一样。最好先 COPY 完所有要操作的文件，然后再 RUN。COPY 指令也同时支持 shell 格式和 exec 格式，但当参数中包含空格时，最好用 exec 格式。
+ VOLUME，和 `docker run` 和 `docker create` 中的 `--volume` 功能类似。数组中的每一项都会用来创建一个 Volume，如本例中相当于 `--volume /var/log`。该指令不能创建 bind-mount Volume，也不能定义只读的 Volume。
+ CMD，它和 ENTRYPOINT 类似，也同时支持 shell 和 exec 两种格式，用于开启容器中的某个进程。显著区别是：CMD 为入口点提供参数列表。容器默认的入口点是 `/bin/sh`。如果入门点已用 exec 格式设置过了，那么可用 CMD 来设置默认参数。本例中，基映像设置的 `ENTRYPOINT ["/app/mailer.sh"]`，而现在的 `CMD ["/var/log/mailer.log"]`，那么容器运行时默认会执行 `/app/mailer.sh /var/log/mailer.log`。

另一个实现是用 AWS 的简单邮件服务来发送邮件，Dockerfile 文件 mailer-live.df 如下：

```conf
FROM dockerinaction/mailer-base:0.6
ADD ["./live-impl", "${APPROOT}"]
RUN apt-get update && \
    apt-get install -y curl python && \
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && \
    python get-pip.py && \
    pip install awscli && \
    rm get-pip.py && \
    chmod a+x "${APPROOT}/${APP}"
RUN apt-get install -y netcat
USER example:example
CMD ["mailer@dockerinaction.com", "pager@dockerinaction.com"]
```

+ ADD，它和 COPY 类似，但它的源文件部分可以是一个 URL，另外当源文件是压缩文件时，可以自动提取。自动解压文件功能很好，但是 URL 下载最好不用，因为它无法清除临时文件，从而增加了层，可以通过串接的 RUN 命令来实现（如以上命令所示）。


# 为下游注入构建时的行为

在基映像的 Dockerfile 中可以使用 ONBUILD 指令，如：

```
ONBUILD COPY [".", "/var/myapp"]
ONBUILD RUN go build /var/myapp
```

这些指令，当在构建基映像本身时不会被执行，但当在构建子映像中，会在执行 `FROM BASE_IMAGE_NAME` 时触发，即在运行 `FROM` 后，会执行这些 `ONBUILD` 指令。

本例子中，先创建一个基映像 ，Dockerfile 文件为 base.df：

```
FROM busybox:latest
WORKDIR /app
RUN touch /app/base-evidence
ONBUILD RUN ls -al /app
```

当用 `docker build` 构建该基映像时，不会运行 `ls -al /app`。

```bash
$ docker build -t dockerinaction/ch8_onbuild -f base.df .
```

子映像的 Dockerfile downstream.df 如下：

```
FROM dockerinaction/ch8_onbuild
RUN touch downstream-evidence
RUN ls -al .
```

构建时会先执行基映像中的 `ls -al /app`，再运行子映像中的 `ls -al .`：

```bash
$ docker build -t dockerinaction/ch8_onbuild_down -f downstream.df .
Sending build context to Docker daemon 4.096 kB
Step 1 : FROM dockerinaction/ch8_onbuild
# Executing 1 build trigger...
Step 1 : RUN ls -al /app
 ---> Running in 226a8fbdb4ad
total 8
drwxr-xr-x    2 root     root          4096 Oct 20 08:38 .
drwxr-xr-x   20 root     root          4096 Oct 20 08:40 ..
-rw-r--r--    1 root     root             0 Oct 20 08:38 base-evidence
 ---> c9869c6c3a51
Removing intermediate container 226a8fbdb4ad
Step 2 : RUN touch downstream-evidence
 ---> Running in 0b1ffa66ed1d
 ---> 8e011e58309e
Removing intermediate container 0b1ffa66ed1d
Step 3 : RUN ls -al .
 ---> Running in 003c80788161
total 8
drwxr-xr-x    2 root     root          4096 Oct 20 08:40 .
drwxr-xr-x   21 root     root          4096 Oct 20 08:40 ..
-rw-r--r--    1 root     root             0 Oct 20 08:38 base-evidence
-rw-r--r--    1 root     root             0 Oct 20 08:40 downstream-evidence
 ---> 5393b3626dce
Removing intermediate container 003c80788161
Successfully built 5393b3626dce
```

# 使用启动脚本及多进程容器

## 环境预先验证

需要验证的内容有：

+ 会用到的连接（别名）
+ 环境变量
+ 网络
+ 网络端口
+ 根文件系统挂载参数（rw 呈 ro)
+ Volumes
+ 当前用户


脚本可以用任何语言实现，但最好用已经包含在了映像中的语言，如 /bin/sh 或 /bin/bash。

如下面的脚本会检测是否有一个开启 80 端口的容器已通过 web 别名关联到本容器了，或者是否已经设置了 WEB_HOST 环境变量：

```bash
#!/bin/bash
set -e

if [ -n "$WEB_PORT_80_TCP" ]; then
    if [ -z "$WEB_HOST" ]; then
        WEB_HOST='web'
    else
        echo >&2 '[WARN]: Linked container, "web" overridden by $WEB_HOST.'
        echo >&2 "===> Connecting to WEB_HOST ($WEB_HOST)"
    fi
fi

if [ -z "$WEB_HOST" ]; then
    echo >&2 '[ERROR]: specify a linked container, "web" or WEB_HOST environment variable'
    exit 1
fi
exec "$@" # run the default command
```

可以利用启动脚本 + 容器重启策略来构建更加可靠的容器。


## 初始化进程

UNIX 的初始化进程（如 init) 负责对其它所有进程的开启、管理、重启、关闭和监测。而容器中最好也用类似的工具来管理进程。

初始化进程通常是用文件来描述初始化系统的状态：

+ 哪些程序要开启
+ 何时开启
+ 当停止后如何操作


使用初始化进程是启动多个程序、清理孤儿进程、监测进程、自动重启失败进程的最佳方式。

系统自带的重量级的初始化系统有 SysV, Upstart, systemd 等。而轻量级的有 runit, BusyBox init, Supervisord, DAEMON Tools 等。

# 构建安全加固的应用映像

通常的做法是尽可以减少映像中包含的组件数。

## 固定基映像的版本

包含摘要的映像 ID 称为 content addressable image identifier（CAIID)。Dockerfile 中的 From 指令通过使用 CAIID，可以确保引用的基映像固定不变。

```
$ docker pull debain:jessie
# output Digest
Digest: sha256:d5e87cfcb730...

# Dockerfile:
FROM debian@sha256:d5e87cfcb730...
...
```

## 用户权限

首先要明白的是话，无法阻止 Docker 用户在容器中使用 root。

最佳实践：

+ 在容器中使用非 root 的用户和组
+ Dockerfile 中通过 USER 指令尽早降低权限
+ 考虑运行时需要的权限和 capabilities
+ 由于容器和主机共享 USR 命名空间，最好不用数字 ID 来引用用户和组，应该为容器重新创建用户和组，如 `RUN groupadd -r postgres && useradd -r -g postgres postgres`。


## SUID 和 SGID 权限

设置了 SUID 的可执行文件按其所有者身份运行，如 `/usr/bin/passwd`。设置了 SGID 的可执行文件按其所有组的组身份运行。

为防止提权，可以将这些可执行文件的 SUID 和 SGID 重置，如：

```bash
RUN for i in $(find / -type f \( -perm +6000 -o -perm +2000 \)); \
    do chmod ug-s $i; done
```

参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Build automation and advanced image considerations](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
