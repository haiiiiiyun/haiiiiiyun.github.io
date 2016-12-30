---
title: 单机上通过 Nginx 反向代理部署多个域名（子域名）的 Docker 应用
date: 2016-12-30
writing-time: 2016-12-30 11:04
categories: programming Docker
tags: Docker Programming nginx domain
---

# 目标

在一台主机上运行多个 Web 应用，每个 Web 应用通过 docker-compose 管理，运行在各自的容器组内。

每个 Web 应用有各自的域名或子域名，通过在浏览器中输入域名，实现对各 Web 应用的访问。

# 方案 1

在单主机上运行一个真实的 Nginx（不在容器时运行），作为反向代理服务器。它针对不同的域名请求，转发给相应的容器。

# 方案 2

在单主机上运行一个容器 Nginx 作为代理服务，在启动该代理服务容器时，必须通过 `--link` 将所有的 Web 应用容器关联过来。由于 Docker 容器关联的实现方式，每次 Web 应用容器重启上，都必须要重启代理服务容器，这将影响到其它 Web 容器的可用性。因此不考虑使用这种方案。

# 具体实现

实验环境是阿里云 ECS Ubuntu 16.04。

## 安装最新版的 nginx:

在 `/etc/apt/sources.list` 中添加源：

```bash
$ sudo vi /etc/apt/sources.list

# add the lines below
deb http://nginx.org/packages/ubuntu/ xenial nginx
deb-src http://nginx.org/packages/ubuntu/ xenial nginx
```

安装：

```bash
$ sudo apt-get update 
$ sudo apt-get install nginx
```

具体流程可参见 [nginx 安装文档](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)。



参考文献： 

+ [一台服务器，两个部署了nginx的容器，解析了两域名，想分别访问这两个容器不添加端口？](https://segmentfault.com/q/1010000007004630)
+ [搭建nginx反向代理用做内网域名转发](http://www.ttlsa.com/nginx/use-nginx-proxy/)
