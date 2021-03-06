---
title: Ubuntu 重装后的初始化设置
date: 2017-08-04
writing-time: 2017-08-04
categories: misc
tags: ubuntu node npm fcitx grub
---

# 更新 apt

```bash
$ sudo apt-get update && sudo apt-get upgrade -y
```

# 更新 Grub 启动延时

```bash
$ sudo vi /etc/default/grub
```

修改 `GRUB_TIMEOUT` 项的值。

再运行：

```bash
$ sudo update-grub
```

# 安装多线程下载工具 axel

```bash
$ sudo apt-get install axel

# download
$ axel -n 5 http://example.com/file.gzip
```

# 安装 Fcitx 五笔拼音输入法

1. 安装汉语语言包和 fcitx

```bash
$ sudo apt-get install language-pack-zh-hans -y

$ sudo apt-get install fcitx-table-wbpy
```

2. 在 "System Settings  -->  Language Support" 中将 "Keyboard input method system: " 设置为 "fcitx"。

3. 在 "System Settings  -->  Text Entry" 中将添加 WubiPinyin(Fcitx)。将 "English(US)" 和 "WubiPinyin(Fcitx)" 的 "Swith to next source using:" 值都设置为 "Control L"。

4. 在 WubiPinyin(Fcitx) 的 "Input Method Configuration" 界面中将 Trigger Input Method 清空，关闭 "Enable Hotkey to scroll Between Input Method"。


# 安装 WPS

下载地址： http://community.wps.cn/download/

ubuntu 16.04 下解决 WPS 无法输入中文的问题：

1. word 部分

在 /usr/bin/wps 的第一行 #!/bin/bash 下添加：

```bash
export XMODIFIERS="@im=fcitx"
export QT_IM_MODULE="fcitx"
```

2. ppt、excel部分

和 word 一样的方法添加环境变量，只是编辑的文件各不同：

```bash
$ vi /usr/bin/wpp
$ vi /usr/bin/et
```


# 安装配置 git

详细文档见 [Generating a new SSH key and adding it to the ssh-agent](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)。

```bash
$ sudo apt-get install git -y  # 安装 git

$ git config --global user.name "Jiang Haiyun" 
$ git config --global user.email "jiang.haiyun@gmail.com"

$ ssh-keygen -t rsa -b 4096 -C "jiang.haiyun@gmail.com" # 创建 ssh key

$ eval "$(ssh-agent -s)"  # 在后台开启 ssh-agent

Agent pid 59566

$ ssh-add ~/.ssh/id_rsa # Add your SSH private key to the ssh-agent

$ sudo apt-get install xclip # Downloads and installs xclip.

$ xclip -sel clip < ~/.ssh/id_rsa.pub # Copies the contents of the id_rsa.pub file to your clipboard
```

之后，可以将 SSH Key 添加到 GitHub 和 Bitbucket 中。


# 恢复系统的配置文件

```bash
$ cd ~/workspace
$ git clone git@github.com:haiiiiiyun/dot-files.git
$ cp ~/workspace/dot-files/bashrc ~/.bashrc
$ cp ~/workspace/dot-files/tmux.conf ~/.tmux.conf
$ cp ~/workspace/dot-files/vimrc ~/.vimrc
$ cp ~/workspace/dot-files/psqlrc ~/.psqlrc
$ cp -r ~/workspace/dot-files/tmuxinator/ ~/.tmuxinator
```

# 安装和配置 VIM

```bash
$ sudo apt-get install vim-gnome -y

# Plugin manager Vundle
$ mkdir -p ~/.vim/bundle && \
$ git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

# 在 VIM 中运行 `:PluginInstall`
```

# 安装 tmux 和 Tmuxinator

```bash
$ sudo apt-get install tmux

# Tmuxinator基于Ruby，首先安装Ruby
$ sudo apt-get install ruby

# gem 版本需在 2.6.x 以上：

$ sudo gem update --system
$ gem -v
2.6.12

# 配置 gem 的 Ruby China 镜像
$ gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/
$ gem sources -l
https://gems.ruby-china.org

$ sudo gem install tmuxinator
```

# 将 "CAPS LOCK" 键设置成 CTRL 键

在 Linux，需对键盘配置文件进行修改：

`sudo vi /etc/default/keyboard`， 找到以 XKBOPTIONS 开头的行，添加 ctrl:nocaps 使 CAPS LOCK 成为另一个 CTRL 键，或者添加 ctrl:swapcaps 使 CAPS LOCK 键和 CTRL 两键的功能相互交换。 

例如，修改后的内容可能为：

`XKBOPTIONS="lv3:ralt_alt,compose:menu,ctrl:nocaps"`

然后运行：

`sudo dpkg-reconfigure keyboard-configuration`。

重启。


# 安装 PostgreSQL

1. 先从 PostgreSQL 下载页 获取相应的 Apt 仓库信息，然后创建文件 /etc/apt/sources.list.d/pgdg.list， 命令为：

```bash
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
```

2. 加载仓库的 GPG Key：

```bash
$ wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
```

3. 安装

```bash
$ sudo apt-get update && sudo apt-get install postgresql-9.5 postgresql-contrib -y
$ sudo apt-get install libpq-dev
```

# Python 开发环境

```bash
$ sudo apt-get install python-pip -y
$ pip install -U pip
$ sudo apt-get install python-dev

$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper

# virtual env dirs
$ mkdir ~/.envs
$ . ~/.bashrc  # 运行 source virtualenvwrapper.sh 来初始化

# 创建 xcity 项目的环境
$ mkvirtualenv xcity
$ workon xcity
$ pip install -f ~/workspace/xcity/requirements/local.txt
```

# 安装 Jupyter

```bash
$ sudo pip install jupyter 

# 安装 Shadowsocks 客户端

```bash
sudo add-apt-repository ppa:hzwhuang/ss-qt5
sudo apt-get update
sudo apt-get install shadowsocks-qt5 -y
```

在 Ubuntu 16.04 中启动时如果出现错误：

ss-qt5: error while loading shared libraries: libQtShadowsocks.so.1: cannot open shared object file: No such file or directory

可创建链接解决：

```bash
$ sudo ln /usr/lib/libQtShadowsocks.so /usr/lib/libQtShadowsocks.so.1
```

SS 共享账号页见 https://doub.bid/sszhfx/。

# 安装 Ext JS 6 开发环境

见 [设置 Ext JS 6 开发环境](http://www.atjiang.com/setting-up-extjs6/)。


# 安装 Docker 和 Docker XAMPP

安装 Docker 见 [在 Ubuntu 上安装 Docker](http://www.atjiang.com/install-docker-on-ubuntu/)。

安装 Docker Compose 见 [安装 Docker Compose 并运行一个简单的 Python Web 应用](http://www.atjiang.com/install-docker-compose-and-run-simple-app/)。


配置阿里云镜像见 [Docker 注册中心及配置阿里云加速](http://www.atjiang.com/docker-registry-and-aliyun-mirror/)。

或者使用 Docker 中国官方镜像加速，见 https://www.docker-cn.com/registry-mirror。

可以在 Docker 守护进程启动时传入 --registry-mirror 参数：

```bash
$ docker --registry-mirror=https://registry.docker-cn.com daemon
```

为了永久性保留更改，可以修改 /etc/docker/daemon.json 文件并添加上 registry-mirrors 键值。

```json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

修改保存后重启 Docker 以使配置生效。


安装配置 Docker 版本的 XAMPP:

Docker 映像文件见: https://hub.docker.com/r/tomsik68/xampp/ 。


```bash
$ docker pull tomsik68/xampp

# 运行
$ docker run --name myXampp -p 9922:22 -p 9980:80 -d -v ~/workspace/www:/www tomsik68/xampp
```

在 .bashrc 中添加 alias:

```bash
# run docker xampp
alias xamppstart='docker run --name myXampp -p 9922:22 -p 9980:80 -d -v ~/workspace/www:/www tomsik68/xampp'
```

# 安装 Node 和 Angular 环境

[Angualr CLI](https://github.com/angular/angular-cli) 要求 node 6.9.x 和 npm 3.x.x。

## 安装 node

在 Ubuntu 16.04 上安装当前稳定版本 v6.x:

```bash
$ curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
$ sudo apt-get install -y nodejs
```

详细参考 https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions 。

配置 npm 使用淘宝镜像：

```bash
$ npm config set registry=http://registry.npm.taobao.org
```

详细见 [npm 等国内镜像整理](http://www.atjiang.com/china-mirrors/)。


## 安装 Angualar CLI

```bash
$ sudo npm install -g @angular/cli
```
