---
title: 如何将 Ubuntu 16 和 18 上的 python 升级到最新 3.8 版
date: 2020-03-10
writing-time: 2020-03-10
categories: python;ubuntu
tags: python;ubuntu
---

# 1. 概述

本文记录在 Ubuntu 16.04 上将 python 升级为 3.8 版本，并配置为系统默认 python3 的过程。

在 Ubuntu 16.04 中，python3 的默认版本为 3.5：

```bash
$ python3 -V
Python 3.5.2
```

本文以在 Ubuntu 16.04 中安装为例，方法同样适用于 Ubuntu 18.04 。

# 2. 通过 Apt 安装

Ubuntu 官方 apt 库中还未收录 python 3.8，这里使用 [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) PPA 库安装。

## 2.1. 安装依赖包

```bash
$ sudo apt update
$ sudo apt install software-properties-common
```

## 2.2. 添加 deadsnakes PPA 源

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa

Press [ENTER] to continue or Ctrl-c to cancel adding it.
```

## 2.3. 安装 python 3.8

```bash
$ sudo apt install python3.8

$ python3.8 -V
Python 3.8.2
```

# 3. 配置 python3.8 为系统默认 python3

**修改默认 python3 会导致打不开 Terminal 等各种问题，解决方法见 [Ubuntu16.04TLS 中终端（Terminal）无法打开的解决办法](https://blog.csdn.net/threeyearsago/article/details/80276579)**


## 3.1. 将 python 各版本添加到 update-alternatives

```bash
$ which python3.8
/usr/bin/python3.8

$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

$ which python3.5
/usr/bin/python3.5

$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 2
```

## 3.2. 配置 python3 默认指向 python3.8

```bash
$ sudo update-alternatives --config python3


There are 2 choices for the alternative python3 (providing /usr/bin/python3).

  Selection    Path                Priority   Status
------------------------------------------------------------
* 0            /usr/bin/python3.5   2         auto mode
  1            /usr/bin/python3.5   2         manual mode
  2            /usr/bin/python3.8   1         manual mode

Press <enter> to keep the current choice[*], or type selection number: 2
```

选择/输入 2, 回车。

## 3.3 测试 python 版本

```bash
$ python3 -V

Python 3.8.2
```

# 资源

+ [How to Install Python 3.8 on Ubuntu 18.04](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
+ [How to upgrade to python 3.7 on Ubuntu 18.10](https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-7-on-ubuntu-18-10/)
