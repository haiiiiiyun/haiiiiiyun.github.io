---
title: Docker 分发公共和私有软件
date: 2016-10-21
writing-time: 2016-10-21 10:27--20:42
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 选择分发方式

分发方式越简单限制越多，越复杂的越灵活。

# 使用托管的注册中心进行发布

服务商有 Docker Hub, Quay.io, Tutum.co 及 Google Container Registry 等。

## 用公共仓库发布：在 Docker Hub 上发布一个 Hello World 映像

先创建映像的 Dockerfile 文件 HelloWorld.df：

```conf
FROM busybox:latest
CMD echo Hello World
```

创建映像：

```bash
$ docker build \
    -t haiiiiiyun/hello-dockerfile \
    -f HelloWorld.df .
```

使用 `docker login` 命令来登录 Docker Hub，该命令的选项有 `--username`，`--email`，`--password`。

最后将映像 push 到 Docker Hub：

```bash
$ docker push haiiiiiyun/hello-dockerfile

The push refers to a repository
[dockerinaction/hello-dockerfile] (len: 1)
7f6d4eb1f937: Image already exists
8c2e06607696: Image successfully pushed
6ce2e90b0bc7: Image successfully pushed
cf2616975b4a: Image successfully pushed
Digest:
sha256:ef18de4b0ddf9ebd1cf5805fae1743181cbf3642f942cae8de7c5d4e375b1f20
```

之后可以通过 `docker search haiiiiiyun/hello-dockerfile` 或者到 Docker Hub 网站上查找该映像。

## 通过自动化构建机制发布公共项目

这种类型的发布工作需要两个部件：

+ 托管的映像仓库，如 Docker Hub
+ 托管的 Git 仓库，用来存放映像源文件，如 github。


Git 仓库提供商，如 github.com 或 bitbucket.org 都提供 webhook。 *webhook*  是 Git 仓库用来向映像仓库发送更新提醒的一种方式。当映像仓库提供商，如 Docker Hub 接收到 webhook 时，它将开启自动化构建映像的过程。其流程如下：

![Docker Hub 自动化构建流程](/assets/images/dockerinaction/docker-hub-automated-build-workflow.png)

举例如下：

先在 Github 上创建一个新的仓库 hello-docker，创建时不要自动生成 licence 和 .gitignore 等文件。

在本地创建目录 hello-docker，在里面创建一个文件 Dockerfile，内容如下：

```conf
FROM busybox:latest
CMD echo Hello World
```

在本地配置 git 项目：

```bash
$ git init
$ git remote add origin \
    git@github.com:haiiiiiyun/hello-docker.git
```

先不要提交，到 https://hub.docker.com/ 页，点击右上角的 "Create -> Create Automated Build"，关联 Github (或 bitbucket) 账号，关联 Github 项目 haiiiiiyun/hello-docker。

现在提交 Git 项目源码后，会在 Docker Hub 上自动构建出映像：

```bash
$ git add Dockerfile
$ git commit -m "first commit"
$ git push -u origin master
```

## 发布私有的托管仓库

和发布公共的托管仓库操作是一样，唯一的区别是在操作前要进行 `docker login`。

下面是登录不同的托管商的例子：

```bash
docker login
# Username: dockerinaction
# Password:
# Email: book@dockerinaction.com
# WARNING: login credentials saved in /Users/xxx/.dockercfg.
# Login Succeeded

docker login tutum.co
# Username: dockerinaction
# Password:
# Email: book@dockerinaction.com
# WARNING: login credentials saved in /Users/xxx/.dockercfg.
# Login Succeeded

docker login quay.io
# Username: dockerinaction
# Password:
# Email: book@dockerinaction.com
# WARNING: login credentials saved in /Users/xxx/.dockercfg.
# Login Succeededdocker login
```

# 私有注册中心

## 使用 registry 映像

Docker Hub 的分发软件（注册中心软件）已经打包成了 *registry* 映像，要想在本地运行私有注册中心，只需运行该映像即可：

```bash
$ docker run -d -p 5000:5000 \
    -v "$(pwd)"/data:/tmp/registry-dev \
    --restart=always --name local-registry registry:2
```

运行后，本地的 `localhost:5000` 就是私有注册中心了，可以用 docker 的 pull, run, tag 等命令与它交互。

这种私有中心没有安全机制，无需用户登录即可操作。

### 将映像从 Docker Hub 复制到私有注册中心

```bash
$ docker pull dockerinaction/ch9_registry_bound # pull from Docker Hub
$ docker images -f "label=dia_excercise=ch9_registry_bound" # verify image is discoverable with label filter

$ docker tag dockerinaction/ch9_registry_bound \
    localhost:5000/dockerinaction/ch9_registry_bound
$ docker push localhost:5000/dockerinaction/ch9_registry_bound # push to local registry
```

### 使用私有注册中心中的映像

```bash
$ docker rmi \
    dockerinaction/ch9_registry_bound \
    localhost:5000/dockerinaction/ch9_registry_bound # remove tagged references

$ docker images -f "label=dia_excercise=ch9_registry_bound" # not found
$ docker  pull localhost:5000/dockerinaction/ch9_registry_bound # pull from registry again
$ docker images -f "label=dia_excercise=ch9_registry_bound" # verify image is discoverable with label filter

$ docker rm -vf local-registry
```

它的用法和 Docker Hub 一致，但是它默认无安全认证，因而只适合在本地使用，不适合远程用户访问。

# 映像的手动分发

分发的基本流程如下：

![典型的手工分发流程](/assets/images/dockerinaction/docker-manual-distribution-workflow.png)

## 基于 FTP 的一个分发的例子

FTP 服务端可免费获取，而其客户端在各系统上都有，因此它很适合用于此。

本例中使用了两个现有映像，一个是 ch9_ftpd，它基于 centos:6 映像，它的容器会自动运行 vsftpd(一种 FTP 服务端软件)，并且允许匿名写操作。另一个映像是 ch9_ftp_client，基于 Alpine Linux 映像，里面安装有 LFTP，并且作为容器运行时的 entrypoint。

假设要分发 registry:2 映像，先从 Docker Hub 上 Pull 下载：

```bash
$ docker pull registry:2
```

运行 FTP 服务器：

```bash
# 该容器中的 FTP 允许匿名写 pub/incoming 目录，不适合在生产环境下用
$ docker run -d --name ftp-transport -p 21:12 dockerinaction/ch9_ftpd
```

将要分发的映像保存为文件：

```bash
$ docker save -o ./registry.2.tar registry:2
```

registry.2.tar 文件将保存映像的元数据、历史等所有数据。这一步后，也可以对文件进行检验和、加密等附加操作。

在容器中开启一个 FTP 客户端 ，将要分发的文件上传到 FTP 服务器：

```bash
$ docker run --rm --link ftp-transport:ftp_server \
    -v "$(pwd)":/data \
    dockerinaction/ch9_ftp_client \
    -e 'cd pub/incoming; put registry.2.tar;exit' ftp_server
```

要想验证是否已将文件上传到了服务器中：

```bash
$ docker run --rm --link ftp-transport:ftp_server \
    -v "$(pwd)":/data \
    dockerinaction/ch9_ftp_client \
    -e "cd pub/incoming; ls; exit" ftp_server

-rw-------    1 14       50       33918464 Oct 21 12:19 registry.2.ta
```

从 FTP 服务器中下载映像文件：

```bash
$ rm registry.2.tar # remove old file
$ docker rmi registry:2

$ docker run --rm --link ftp-transport:ftp_server \
    -v "$(pwd)":/data \
    dockerinaction/ch9_ftp_client \
    -e 'cd pub/incoming; get registry.2.tar; exit' ftp_server
```

现在，已经将 registry.2.tar 下载到本地了，可以用 `docker load -i registry.2.tar` 将它转换成映像。

# 映像源文件 (Dockerfile) 的分发流程

1. 项目作者将源码存储到 Github 上，源码中包含有构建映像所需的 Dockerfile 文件
2. 其他人 clone 该项目，根据 Dockerfile 使用 `docker build` 构建出映像


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Public and private software distribution](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
