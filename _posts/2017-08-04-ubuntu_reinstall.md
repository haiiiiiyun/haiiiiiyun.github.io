---
title: Ubuntu 重装后的初始化设置
date: 2017-08-04
writing-time: 2017-08-04
categories: misc
tags: ubuntu
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

# 安装 Fcitx 五笔拼音输入法

1. 安装汉语语言包和 fcitx

```bash
$ sudo apt-get install language-pack-zh-hans -y

$ sudo apt-get install fcitx-table-wbpy
```

2. 在 "System Settings  -->  Language Support" 中将 "Keyboard input method system: " 设置为 "fcitx"。

3. 在 "System Settings  -->  Text Entry" 中将添加 WubiPinyin(Fcitx)。将 "English(US)" 和 "WubiPinyin(Fcitx)" 的 "Swith to next source using:" 值都设置为 "Control L"。

4. 在 WubiPinyin(Fcitx) 的 "Input Method Configuration" 界面中将 Trigger Input Method 清空，关闭 "Enable Hotkey to scroll Between Input Method"。


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
