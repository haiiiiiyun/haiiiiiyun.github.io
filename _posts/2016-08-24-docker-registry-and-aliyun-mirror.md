---
title: Docker 注册中心及配置阿里云配置加速
date: 2016-08-24
writing-time: 2016-08-24 10:46--11:20
categories: programming
tags: Docker Programming Utility
---

[Docker Hub](https://hub.docker.com/) 是由 Docker 公司维护的公共注册中心。

# Docker Hub 相关命令

如 docker search, pull, login, push 等。

# 帐号创建和登录

到 Docker Hub 上注册帐号，在 CLI 中登录：

```shell
$ docker login
```

登录认证信息会保存在 **~/.docker/config.json** 中。

# 搜索并下载映像

```shell
$ docker search centos

$ docker pull centos
```

# 发布

```shell
$ docker push yourname/newimage
```

# 阿里云的 Docker 镜像服务

[Ali-OSM](http://mirrors.aliyun.com/help/docker-engine?spm=0.0.0.0.Xf8pOS)

注册阿里去主机，获取专属加速地址： https://w7snjp9s.mirror.aliyuncs.com

## 安装或升级Docker

请安装 1.6.0 以上版本的 Docker。
可以通过阿里云的镜像仓库下载： mirrors.aliyun.com/help/docker-engine

```shell
curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh - 
```

## 配置 Docker 加速器

可以使用如下的脚本将 mirror 的配置添加到 docker daemon 的启动参数中。
如果系统是 Ubuntu 12.04 14.04，Docker 1.9 以上:


```shell
$ echo "DOCKER_OPTS=\"\$DOCKER_OPTS --registry-mirror=https://w7snjp9s.mirror.aliyuncs.com\"" | sudo tee -a /etc/default/docker sudo service docker restart 
```


如果系统是 Ubuntu 15.04 16.04，Docker 1.9 以上:


```shell
$ sudo mkdir -p /etc/systemd/system/docker.service.d
$ sudo tee /etc/systemd/system/docker.service.d/mirror.conf <<-'EOF'
[Service]
ExecStart= ExecStart=/usr/bin/docker daemon -H fd:// --registry-mirror=https://w7snjp9s.mirror.aliyuncs.com 
EOF
$ sudo systemctl daemon-reload 
$ sudo systemctl restart docker
```

> 参考文献： 
> [Docker docs: Store images on Docker Hub](https://docs.docker.com/engine/tutorials/dockerrepos/) 及 https://cr.console.aliyun.com/?spm=5176.1971733.2.1.gSiNsr#/accelerator
