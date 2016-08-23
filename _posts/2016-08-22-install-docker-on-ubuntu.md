---
title: 在 Ubuntu 上安装 Docker 及其基本使用
date: 2016-08-22
writing-time: 2016-08-22 13:17--22:24
categories: programming
tags: Docker
---

# Ubuntu

Docker 支持的 Ubuntu 版本：

+ Ubuntu Xenial 16.04 (LTS)
+ Ubuntu Wily 15.10
+ Ubuntu Trusty 14.04 (LTS)
+ Ubuntu Precise 12.04 (LTS)


# 先决条件

64 位 Ubuntu, 内核版本最低为 3.10。

检查当前内核版本：

```shell
$ uname -r
4.4.0-34-generic
```

## 更新 apt 源

Docker 默认 APT 仓库中的版本较低，因此要设置 APT 使用 Docker 的官方源：

1. 更新包信息，确保 APT 能使用 **https** 的方式，并安装 CA 证书：

```shell
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
```

2. 添加 GPG 密钥：

```shell
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

3. 添加源：

在文件 */etc/apt/sources.list.d/docker.list* 中添加相应的源。

对应的源有：

+ Ubuntu Precise 12.04 (LTS): `deb https://apt.dockerproject.org/repo ubuntu-precise main`
+ Ubuntu Trusty 14.04 (LTS): `deb https://apt.dockerproject.org/repo ubuntu-trusty main`
+ Ubuntu Wily 15.10: `deb https://apt.dockerproject.org/repo ubuntu-wily main`
+ Ubuntu Xenial 16.04 (LTS): `deb https://apt.dockerproject.org/repo ubuntu-xenial main`


例如，对于 16.04 系统：

```shell
$ echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
```

4. 更新 APT 包索引

```shell
$ sudo apt-get update
```

5. 如果以前有安装过，先清除旧的包

```shell
$ sudo apt-get purge lxc-docker
```

6. 确保 APT 现在是从设置的仓库中下载 Docker 的

```shell
$ apt-cache policy docker-engine
```

执行后的输出如下：

```
docker-engine:
  Installed: (none)
  Candidate: 1.11.1-0~xenial
  Version table:
     1.11.1-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
     1.11.0-0~xenial 500
        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
```

**Ubuntu 不同版本的先决条件**

对于 Ubuntu 14.04, 15.10, 16.04，推荐安装 **linux-image-extra-*** 内核包。这些包能允许我们使用 aufs 存储驱动。

安装命令：

```shell
$ sudo apt-get update && sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
```

## 安装

```shell
$ sudo apt-get install -y docker-engine
```

这里的 -y 参数表示安装过程中的问题全部默认回答 yes。


开启守护进程：

```shell
$ sudo service docker start
```

确认 docker 已经正确安装了：

```shell
$ sudo docker run hello-world
```

该命令会下载一个测试映像然后开启一个容器运行。当容器运行后，会输出一段消息然后退出。

查看 docker 守护进程的状态：

```shell
$ sudo systemctl status docker
```

输出的内容类似：

```
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2016-05-01 06:53:52 CDT; 1 weeks 3 days ago
     Docs: https://docs.docker.com
 Main PID: 749 (docker)
```

# 可选配置

## 无需使用 sudo 执行 docker 命令

**docker** 守护进程绑定到一个 Unix socket，这个 socket 默认由 root 所有。因此，docker 防护进程都是以 root 运行的，其他用户要访问 docker 都需要用 **sudo**。

要想避免输入 sudo, 只需将用户添加到 docker 组中，该组在 Docker 安装时自动创建。

```shell
$ sudo usermod -aG docker $(whoami)
```

之后重新登录，再运行 `$ docker run hello-world` 进行测试。

如果出现如下错误：

```
Cannot connect to the Docker daemon. Is 'docker daemon' running on this host?
```

确保你的 shell 中没有设置 **DOCKER_HOST** 环境变量，如果设置了，就删除掉。

## 开启 UFW 转发

Docker 使用桥接来管理容器的网络。[UFW-Uncomplicated Firewall](https://help.ubuntu.com/community/UFW) 默认会丢弃所有的转发包。因此，当开启 UFW 后，必须对其转发策略进行调整。

同时，UFW 默认还拒绝所有的流入流量，如果想从其它主机连接容器上的端口，也必须进行调整。当 TLS 开启后，Docker 的默认端口是 2376，没有开启时是 2375，默认是没有开启的。

配置 UTW 允许连接 Docker 端口：

1. 确认 UFW 是否安装和开启了

```shell
$ sudo ufw status
```

2. 在 **/etc/default/ufw** 文件中，修改转发策略：

```conf
DEFAULT_FORWARD_POLICY="ACCEPT"
```

3. 重新加载 ufw

```shell
$ sudo ufw reload
```

4. 允许连接到 Docker 端口

```shell
$ sudo ufw allow 2375/tcp
```

## 为 Docker 配置 DNS 服务器

桌面系统在 **/etc/resolv.conf** 文件中设置 **127.0.0.1** 为默认的 nameserver，然后 NetworkManager 会设置 dnsmasq 来使用真正的 DNS 服务器。

当在桌面系统上启动 Docker 时，会出现：

```
WARNING: Local (127.0.0.1) DNS resolver found in resolv.conf and containers
can't use it. Using default external servers : [8.8.8.8 8.8.4.4]
```

这是因为 Docker 不能使用本地 DNS 域名服务器。去除该警告的方法是在 **/etc/default/docker** 文件中设置 Docker 的 DNS 服务器：

```conf
DOCKER_OPTS="--dns 8.8.8.8 --dns 192.168.1.1"
```

## 设置系统启动时自动开启 Docker

15.04 及以下系统：

```shell
$ sudo systemctl enable docker
```

14.10 及以下版本在安装  Docker 后就已经通过 upstart 配置为自动启动了。

# 升级 Docker

```shell
$ sudo apt-get upgrade docker-engine
```

# 删除

删除 Docker 包：

```shell
$ sudo apt-get purge docker-engine
```

删除其相关的依赖包：

```shell
$ sudo apt-get autoremove --purge docker-engine
```

以上的命令不会删除映像、窗口、数据卷、用户配置文件等。如果要删除，用：

```shell
$ rm -rf /var/lib/docker
```

# 使用 Docker

## 使用 Docker 命令

语法格式：

```shell
$ docker [option] [command] [arguments]
```

直接键入 `docker` 会列出所有支持的命令。

要查看 docker 子命令的相关帮助文档：

```shell
$ docker docker-subcommand --help
```

要查看 Docke 的系统级信息：

```shell
$ docker info
```

## 使用 Docker 映像

检查是否能从 Docker Hub 下载映像：

```shell
$ docker run hello-world
```

该命令会输出：

```
Hello from Docker.
This message shows that your installation appears to be working correctly.
...
```

看到这些输出，表明 Docker 已经能正常运行了。


通过 search  子命令搜索 Docker Hub 上的映像：

```shell
$ docker search ubuntu
```

会列出匹配的映像列表：

```
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
ubuntu                            Ubuntu is a Debian-based Linux operating s...   3808      [OK]       
ubuntu-upstart                    Upstart is an event-based replacement for ...   61        [OK]       
torusware/speedus-ubuntu          Always updated official Ubuntu docker imag...   25                   [OK]
...
```

找到后，用 pull 子命令将映像下载下来：

```shell
$ docker pull ubuntu
```

下载完成后，使用 run 命令启动包含该映像的一个容器：

```shell
$ docker run ubuntu
```

要查看主机所有已下载的映像：

```shell
$ docker images
```

该命令会列出如下列表：

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              c5f1cf30c96b        7 days ago          120.8 MB
hello-world         latest              94df4f0ce8a4        2 weeks ago         967 B
```


## 运行容器

```shell
$ docker run -it ubuntu
```

该命令启动了一个 ubuntu 容器，然后通过 **-i** 开关指定在容器中开启一个可交互的 shell，运行后如下：

```
root@d9b100f2f636:/#
```

在命令行中可以看到容器的 id 号，比如本例中是 **d9b100f2f636**，同时可以看到容器中的用户具有 root 权限。之后，可以在该 shell 中执行任何程序。

## 将容器中的修改提交到 Docker 映像中

Docker 文件系统默认是临时的。当你从一个映像启动一个容器后，可以在其中创建、修改和删除文件，就像在虚拟机上的操作一样。但是，一旦你关闭容器再重启后，之前在容器中的所有更改都会被还原。这是因为映像只是一个模板。要想保存修改，需要通过使用 Docker Data Volumes，将容器的状态保存为一个新的映像。

先退出 Docker:

```shell
$ exit
```

再将当前的容器更新提交到 Docker Hub 上：

```shell
$ docker commit -m "What did you do to the image" -a "Author Name" container_id reposity/new_image_name
```

## 列出 Docker 容器

Docker 运行一段时间后，会有很多的容器。

列出所有的活跃容器：

```shell
$ docker ps
```

列出所有的容器：

```shell
$ docker ps -a
```

列出最近创建的容器：

```shell
$ docker ps -l
```

停止容器：

```shell
$ docker stop container_id
```

## 将映像推送个一个 Docker 仓库

例如推送到 Docker Hub。先登录 Docker Hub：

```shell
$ docker login -u docker-registry-username
```

然后进行推送：

```shell
$ docker push docker-registry-username/docker-image-name
```

> 参考文献： [Docker docs](https://docs.docker.com/engine/installation/linux/ubuntulinux/) 以及 [how-to-install-and-use-docker-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
