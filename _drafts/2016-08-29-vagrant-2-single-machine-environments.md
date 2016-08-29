---
title: 设置 Vagrant 单机环境
date: 2016-08-29
writing-time: 2016-08-29 10:50
categories: programming
tags: Vagrant Utility Vagrant&nbsp;Virtual&nbsp;Development&nbsp;Environment&nbsp;Cookbook
---

# 定义一个单机 Vagrant 环境

这是最基本的一个定义模式，定义一个单机环境，并通过 `vagrant up` 命令来管理。

## 简单 Vagrant 环境

1. 通过 `vagrant init` 来初始化一个 Vagrant 环境。这将生成一个 Vagrantfile 文件，并且附有一条定义：

```conf
config.vm.box = "base"
```

2. 为该环境设置 box：

```conf
config.vm.box = "puppetlabs/ubuntu-14.04-64-nocm"
```

3. 通过 `vagrant up` 命令开启虚拟环境。如果之前没有缓存 box，该命令可能会下载。

## 自定义的单机环境

1. 通过 `vagrant init` 初始化，并生成 Vagrantfile 文件

2. 定义环境。先删除 `config.vm.box="base"` 行及注释行，清理后内容如下：

```conf
# -*- mode: ruby -*-
# vi: set ft=ruby
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
end
```

3. 在主配置块中添加机器定义，现在完整文件内容如下：

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define "web" do |web|
    web.vm.box = config.vm.box = "puppetlabs/ubuntu-14.04-64-nocm"
  end
end
```

这里，先定义机器名 "web"，而 `|web|` 是 Ruby 定义一个块的语法，块中的代码变量的作用哉只局限在块中。

启动这个命名机器用：

```shell
$ vagrant up web
```

在机器定义语句中也可以传送一个 `primary` 选项，设置后在启动机器时就不需要指定机器名字了，直接用 `vagrant up`，这时的配置文件如下：

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define "web", primary: true do |web|
    web.vm.box = config.vm.box = "puppetlabs/ubuntu-14.04-64-nocm"
  end
end
```

+ 配置对象是 Vagrantfile 的基本单元，每个 Vagrantfile 都需要最少一个配置对象。一个配置对象表示一台虚拟机，添加到该配置对象上的操作将定义该虚拟机上的操作及任何针对该虚拟机要执行的操作。

+ Vagrantfile 和 配置对象都以 Ruby 语法进行定义。


# Vagrant 机器中的端口转发

1. 如上节中定义一个 web 虚拟机。

2. 定义端口转发，将虚拟机上的 80 端口 重定向为 主机上的 8888 端口：

```ruby
config.vm.define "web", primary: true do |web|
    web.vm.box ="puppetlabs/ubuntu-14.04-32-nocm"
    web.vm.network "forwarded_port", guest:80, host:8888
end
```

3. 使用 `provision` 命令在虚拟机上安装 nginx 服务：

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.define "web", primary: true do |web|
        web.vm.box ="puppetlabs/ubuntu-14.04-32-nocm"
        web.vm.network "forwarded_port", guest:80, host:8888
        web.vm.provision "shell", inline: "apt-get install -y nginx"
    end
end

4. 开启并在主机的浏览器上访问 `http://localhost:8888`。

+ `forwarded_port` 选项利用 **端口转发** 技术，该技术通常用于服务器上实现为同一台主机上的多台虚拟机响应请求。在设置端口转发时，如果指定的主机端口已被其它程序占用，则会出现 **端口冲突**，这可以通过使用 *auto_correct* 选项来修改，当出现端口冲突时，自动选取一个新的端口业使用。

# 用 Vagrant 开启一个 GUI

关键是安装一个有 GUI 环境的虚拟机。











> 参考文献： 
> [Vagrant Virtual Development Environment Cookbook](https://www.packtpub.com/virtualization-and-cloud/vagrant-virtual-development-environment-cookbook)
