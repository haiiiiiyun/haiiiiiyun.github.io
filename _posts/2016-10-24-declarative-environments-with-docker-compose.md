---
title: Docker 分发公共和私有软件
date: 2016-10-24
writing-time: 2016-10-24 09:07
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# Docker Compose

Compose 是一个用来定义、启动和管理服务的工具，而一个或多个 Docker 容器的组合被定义为一个服务。服务定义在 YAML 文件中，并被 docker-compose 程序管理。

Compose 能用来描述整合的环境及所有服务组件间的交互。

## 简单操作

本例用 Compose 管理一个 WordPress 环境。

新建一个目录 wp-example，在其中创建 docker-compose.yml:

```yaml
wordpress: # defines service named wordpress
  image: wordpress:4.2.2
  links:
    - db:mysql # Models link dependency on db service
  ports:
    - 8080:80 #Maps port 80 on container to port 8080 on host

db: # defines service named db
  image: mariadb
  environment:
    MYSQL_ROOT_PASSWORD: example # Sets administrative db password through env variable
```

在 wp-example 目录下使用 `docker-compose up` 来开启所有服务 :

```bash
$ docker-compose up

Creating wpexample_db_1...
Creating wpexample_wordpress_1...
```

可以使用的命令或快捷键：

+ 用 `Ctrl-C` 关闭全部服务
+ `docker-compose ps` 只列出本目录下的 docker-compose.yml 管理的容器
+ `docker-compose stop [name]` 或 `docker-compose kill [name]` 停止管理的容器或某个特定容器
+ `docker-compose rm [name]` 删除管理的所有容器或某个特定容器, 其 `-f` 选项不是强制删除的意思，而是不显示验证阶段, `-v` 选项将一并删除其 Volume


## 一个复杂的结构：注册中心和 Elasticsearch 集成











参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Declarative environments with Docker Compose](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
