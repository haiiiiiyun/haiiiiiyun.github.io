---
title: Config  Python PyPi mirrors
date: 2023-11-15
tags: python pip mirrors
categoris: Programming
---

## Location of configuration files

Pip has 3 levels of configuration files:

+ `global`: system-wide configuration files, shared across users: `/etc/pip.conf`
+ `user`: per-user, locates in `~/.pip/pip.conf`
+ `site`: per-environment configuration file; i.e. per-virtualenv, locates in `$VIRTUAL_ENV/pip.conf`

## Content of configuration file

Here we set up an aliyun mirror.

```conf
[global]
trusted-host=mirrors.aliyun.com
index-url=https://mirrors.aliyun.com/pypi/simple
```

Following are some mirrors in China:

+ https://pypi.tuna.tsinghua.edu.cn/simple/
+ http://mirrors.aliyun.com/pypi/simple/
+ https://pypi.mirrors.ustc.edu.cn/simple/
+ http://pypi.hustunique.com/simple/
+ https://mirror.sjtu.edu.cn/pypi/web/simple/
+ http://pypi.douban.com/simple/

## Config mirror for a Docker container

We can copy an existing pip.conf to a Docker container under `/etc/`.

Just  add a `COPY` instruction in Dockerfile as following, assuming we already have a config file at `./requirements/pip.conf`:

```yaml
COPY ./requirements/pip.conf /etc/pip.conf
COPY ./requirements/ /requirements

RUN pip install -r /requirements/production.txt
```

## Install a package from a mirror temporarily

```bash
$ pip install package-name -i mirror-url
```

## Links

https://pip.pypa.io/en/stable/topics/configuration/#config-file
https://developer.aliyun.com/mirror/