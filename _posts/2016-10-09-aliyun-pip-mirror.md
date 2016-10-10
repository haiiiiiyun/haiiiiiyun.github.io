---
title: 阿里云服务器设置 Python PyPi 镜像源
date: 2016-10-09
writing-time: 2016-10-09 21:56--22:34
categories: python
tags: Programming Python Aliyun
---

阿里云 ECS 服务器（青岛）下载 PyPi 中的资源相当慢，需要配置 Pip 的镜像源。


# 配置文件的位置

+ 全局的位于 `/etc/pip.conf`
+ 用户级别的位于 `$HOME/.pip/pip.conf`
+ 每个 virtualenv 也可以有自己的配置文件 `$VIRTUAL_ENV/pip.conf`


# 配置文件的内容

```
[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple
```

若使用阿里云服务器，可将源的域名从 mirrors.aliyun.com 改为 mirrors.aliyuncs.com, 这样就不会占用公网流量。

# 配置 Docker 容器中的源

如果 Docker 容器中也需要下载 Pip 中的资源，可以将 pip.conf 复制到容器中的 /etc/ 目录。

方法是在 Dockerfile 文件中使用 `COPY` 命令（假设 pip.conf 位于源码目录中的 requirements/ 下)：

```bash
COPY ./requirements/pip.conf /etc/pip.conf
COPY ./requirements/ /requirements

RUN pip install -r /requirements/production.txt
```

参考：

+ [p://pip.pypa.io/en/stable/user_guide/#config-file](https://pip.pypa.io/en/stable/user_guide/#config-file)
+ [mirrors.aliyun.com](http://mirrors.aliyun.com/)
