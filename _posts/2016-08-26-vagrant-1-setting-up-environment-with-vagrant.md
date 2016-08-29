---
title: 使用 Vagrant 设置你的环境
date: 2016-08-26
writing-time: 2016-08-26 15:23
categories: programming
tags: Vagrant Utility Vagrant&nbsp;Virtual&nbsp;Development&nbsp;Environment&nbsp;Cookbook
---

# 简介

通过 Vagrant，团队间开发环境的共享不再需要复制虚拟机映像，只需从源码库中找出 vagrant 配置文件 Vagrantfile，然后运行 `vagrant up`。

Vagrantfile 文件作用：

+ 定义虚拟机
+ 配置虚拟机如何与外界交互
+ 定义虚拟机上安装什么软件

# 安装 Vagrant 和 VirtualBox

1. VirtualBox [下载地址](http://virtualbox.org)。

2. RubyGems 中的 Vagrant 版本会较旧，最好到 [官方下载安装](https://www.vagrantup.com/downloads.html)，要安装 1.5 及以上版本。

3. 安装后运行 `vagrant version` 确保安装成功。

Vagrant 是一个虚拟机的管理框架，它不是用来创建和托管虚拟机的。

# 初始化第一个环境

1. 指定虚拟系统的 box 文件名，并在当前目录下创建相应的 Vagrantfile 配置文件：

```shell
$ vagrant init boxcutter/ubuntu1604-i386 # 32 位系统
```

```shell
$ vagrant init ubuntu/xenial64 # 64 位系统
```


2. 开启虚拟机

```shell
$ vagrant up --provider virtualbox
```

如果虚拟系统 box 文件在当前系统缓存中未找到，会自动到网上下载。

要将虚拟系统 box 文件事先添加到系统缓存中，可以用：

```shell
$ vagrant box add box_name
```

如果没有指定地址，默认都是从 [atlas hashicorp](https://atlas.hashicorp.com/) 下载的。我们也可以将 box 文件放在自己的服务上，然后这样下载添加到缓存中：

```shell
$ vagrant box add http://servername/boxes/environment.box
```

# 查找虚拟系统 box 文件

更多 box 文件，可以到 [atlas hashicorp](https://atlas.hashicorp.com/ubuntu/boxes/xenial64) 查找。

# 将现有的虚拟机映像转成 box 文件

例如 VirtualBox 上已安装配置了 CentOS 6.5 系统，且在 VirtualBox 虚拟机列表上的名字为 CentOS，用户名为 uaccount, 密码为 passw0rd。

打包：

```shell
$ vagrant package --base=CentOS --output=centos64.box

==> CentOS: Exporting VM...
```

要将打包好的 box 文件添加到缓存中：

```shell
$ vagrant box add centos64.box --name=centos64
```

Vagrant box 文件实际上是一个 TAR 文件，如果用 untar 命令解开后，可以看到：

```
-rw------- 0 cothomps staff 1960775680 Jul 24 20:42 ./box-disk1.vmdk
-rw------- 0 cothomps staff 12368 Jul 24 20:38 ./box.ovf
-rw-r--r-- 0 cothomps staff 505 Jul 24 20:42 ./Vagrantfile
```

其中 .mvdk 是 VirtualBox 的虚拟硬盘文件，.ovf 定义了虚拟机的一些属性，而 ./Vagrantfile 则定义了 MAC 地址等信息，我们也可以在添加定制的其它文件。


> 参考文献： 
> [Vagrant Virtual Development Environment Cookbook](https://www.packtpub.com/virtualization-and-cloud/vagrant-virtual-development-environment-cookbook)
