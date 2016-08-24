---
title: 安装 Docker Compose 并运行一个简单的 Python Web 应用
date: 2016-08-24
writing-time: 2016-08-24 16:46--17:23
categories: programming
tags: Docker
---

# 安装

```shell
$ sudo -i
$ curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
$ chmod +x /usr/local/bin/docker-compose
```

# 运行一个简单的 Python Web 应用

## 步骤1：设置

1. 创建项目目录：

```shell
$ mkdir composetest
$ cd composetest
```

2. 在项目目录中创建 app.py:

```python
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

3. 在项目目录下创建 requirements.txt 定义依赖，内容如下：

```conf
flask
redis
```

## 步骤 2：创建一个 Docker 映像文件

1. 在项目目录下创建 Dockerfile 文件，内容如下：

```conf
FROM python:2.7
ADD . /code
WORKON /code
RUN pip install -r requirements.txt
CMD python app.py
```

该文件告诉 Docker：

+ 基于 Python 2.7 映像开始构建新映像
+ 将当前目录挂载到映像的 /code 目录
+ 设置映像的工作目录为 /code
+ 安装 Python 依赖文件
+ 设置容器默认运行的命令 python app.py


再创建一个名为 web 的新映像文件：

```shell
$ docker build -t web .
```

## 步骤 3：定义服务

使用 docker-compose.yml 来定义一组服务：

1, 在项目目录中创建 docker-compose.yml 文件，内容如下：

```yaml
version: '2'
services:
  web:
    build: .
    ports:
     - "5000:5000"
    volumes:
     - .:/code
    depends_on:
     - redis
  redis:
    image: redis
```

该文件定义了两个服务: web 和 redis。

针对 web 服务：

+ 将从当前目录下的 Dockerfile 文件构建出 web 映像
+ 将主机的 5000 端口映射到容器中的 5000 端口
+ 将主机的当前目录挂载到容器的 /code 目录，从而当代码修改后，无需重建映像
+ 将 web 服务与 redis 服务连接起来


## 步骤 4：构建并用 Compose 运行应用

1. 在项目目录下，开启应用：

```shell
$ docker-compose up

Pulling image redis...
Building web...
Starting composetest_redis_1...
Starting composetest_web_1...
redis_1 | [8] 02 Jan 18:43:35.576 # Server started, Redis version 2.8.3
web_1   |  * Running on http://0.0.0.0:5000/
web_1   |  * Restarting with stat
```

之后，就能通过 5000 端口进行访问了。

## 步骤 5：实验其它的命令

通过使用 `-d` 使服务在后端运行，通过 `docker-compose ps` 来查看当前运行的服务：

```shell
$ docker-compose up -d
Starting composetest_redis_1...
    Starting composetest_web_1...
    $ docker-compose ps
    Name                 Command            State       Ports
    -------------------------------------------------------------------
    composetest_redis_1   /usr/local/bin/run         Up
    composetest_web_1     /bin/sh -c python app.py   Up      5000->5000/tcp
```

通过 `docker-compose run` 可以在服务上运行一次性命令，例如查看 web 服务上的环境变量：

```shell
$ docker-compose run web env
```

对应 `docker-compose up -d`，停止用 `docker-compose stop`。


> 参考文献： 
> [Docker docs: Install Docker Compose](https://docs.docker.com/compose/install/)
和 [Docker docs: Getting Started Docker Compose](https://docs.docker.com/compose/gettingstarted/)
