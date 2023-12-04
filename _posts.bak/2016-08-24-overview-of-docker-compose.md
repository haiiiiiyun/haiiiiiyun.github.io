---
title: Docker Compose 概述
date: 2016-08-24
writing-time: 2016-08-24 15:18--16:36
categories: programming
tags: Docker Programming Utility
---

# Docker Compose 概述

Compose 是一个用于定义和运行多容器应用的工具。使用 Compose, 可以通过 Compose 文件对应用中的各种服务进行配置。然后，只需键入一个命令，就能根据配置文件创建并启动所有服务。

Compose 对于开发、测试、Staging 等环境及 CI 工作流都很有用。

使用 Compose 基本上只有三个步骤：

1. 使用 Dockerfile 文件定义应用的环境
2. 在 docker-compose.yml 中定义应用所依赖的所有服务，从而使它们能在各自隔离的环境中协同运作
3. 最后运行 `docker-compose up` 开启应用及其相关的所有服务

docker-compose.yml 文件看起来会像这样：

```yaml
version: '2'
services:
  web:
    build: .
    ports:
    - "5000:5000"
    volumes:
    - .:/code
    - logvolume01:/var/log
    links:
    - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```

Compose 命令可以对应用的整个生命周期进行管理：

+ 开启、关闭和重建服务
+ 查看运行中的服务状态
+ 查看运行中的服务日志
+ 在服务中运行一次性命令

# Compose 的功能

## 在单台主机上实现多个隔离的环境

Compose 使用项目名来对各环境进行分隔：

+ 在开发主机上，可以创建某个环境的多个拷贝（例如为各功能分支运行各自的 Stage）
+ 在 CI 服务器上，为使构建过程互不干扰，可以用唯一的构建编号来设置项目名


默认的项目名是工程目录名，但可以用 `-p` 命令选项或 `COMPOSE_PROJECT_NAME` 环境变量来设置。

## 创建容器时会保留 Volume 中的数据

Compose 会保留你的各种服务所使用的 Volume。当 `docker-compose up` 运行后，如果发现容器之前有运行过，会将旧容器中的 Volume 数量复制到新容器中，以确保你在 Volume 中的数据不会丢失。

## 当有修改才会真正创建新容器

当创建容器时，Compose 对其配置信息进行缓存。当重启容器时，如果容器没有修改，Compose 将重用这些现有容器。

## 变量

Compose 支持在 Compose 文件中使用变量。通过变量可以针对不同的环境或用户实现定制。

# 常见用例

## 开发环境

Compose file 可以对应用所需的所有依赖服务（数据库、队列、缓存、API 等）进行描述和配置。通过 Compose 命令行工具可以创建和开启一个或多个服务容器。

同时，使用 Compose 后，只需一个 Compose 文件及几个命令就能开启一个开发环境。

## 自动化测试环境

Compose 能非常便捷地为你的测试创建和销毁隔离的测试环境。在 Compose file 中对环境进行定义后，只需以下命令就能创建并销毁这些环境：

```shell
$ docker-compose up -d
$ ./run_tests
$ docker-compose down
```

## 单机部署

可以使用 Compose 将项目部署到远程的 Docker 上。


> 参考文献： 
> [Docker docs: Overview of Docker Compose](https://docs.docker.com/compose/overview/)
