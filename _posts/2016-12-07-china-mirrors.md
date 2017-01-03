---
title: npm 等国内镜像整理
date: 2016-12-07
writing-time: 2016-12-07 12:42
categories: programming
tags: Programming Node.js npm Pypi docker
---

# NodeJS

## npm 的淘宝镜像

使用方法 1： 使用 --registry。

```bash
$ npm install gitbook-cli -g --registry=http://registry.npm.taobao.org 
```

使用方法 2：设置 registry。

```bash
$ npm config set registry=http://registry.npm.taobao.org
```

使用方法 3：使用 cnpm。

用 cnpm 命令代替 npm。

先用 npm 安装 cnpm:

```bash
$ npm install -g cnpm --registry=https://registry.npm.taobao.org
```

或者直接通过添加 npm 参数 alias 一个新命令:

```bash
alias cnpm="npm --registry=https://registry.npm.taobao.org \
--cache=$HOME/.npm/.cache/cnpm \
--disturl=https://npm.taobao.org/dist \
--userconfig=$HOME/.cnpmrc"

# Or alias it in .bashrc or .zshrc
$ echo '\n#alias for cnpm\nalias cnpm="npm --registry=https://registry.npm.taobao.org \
  --cache=$HOME/.npm/.cache/cnpm \
  --disturl=https://npm.taobao.org/dist \
  --userconfig=$HOME/.cnpmrc"' >> ~/.zshrc && source ~/.zshrc
```

参考 [npm.taobao.org](https://npm.taobao.org/)，[加速 npm](https://yq.aliyun.com/articles/47269)


# Python

## PyPi 的阿里云镜像


### 配置文件的位置

+ 全局的位于 `/etc/pip.conf`
+ 用户级别的位于 `$HOME/.pip/pip.conf`
+ 每个 virtualenv 也可以有自己的配置文件 `$VIRTUAL_ENV/pip.conf`


### 配置文件的内容

```
[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple
```

若使用阿里云服务器，可将源的域名从 mirrors.aliyun.com 改为 mirrors.aliyuncs.com, 这样就不会占用公网流量。

### 配置 Docker 容器中的源

如果 Docker 容器中也需要下载 Pip 中的资源，可以将 pip.conf 复制到容器中的 /etc/ 目录。

方法是在 Dockerfile 文件中使用 `COPY` 命令（假设 pip.conf 位于源码目录中的 requirements/ 下)：

```bash
COPY ./requirements/pip.conf /etc/pip.conf
COPY ./requirements/ /requirements

RUN pip install -r /requirements/production.txt
```

参考： [阿里云服务器设置 Python PyPi 镜像源](http://www.atjiang.com/aliyun-pip-mirror/), [pip.pypa.io/en/stable/user_guide/#config-file](https://pip.pypa.io/en/stable/user_guide/#config-file), [mirrors.aliyun.com](http://mirrors.aliyun.com/)

# Ruby

## gem 的 Ruby China 镜像

gem 的版本建议在 2.6.x 以上：

```bash
$ gem update --system # 这里要翻墙
$ gem -v
2.6.3

$ gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/
$ gem sources -l
https://gems.ruby-china.org
# 确保只有 gems.ruby-china.org
```

## gem 的清华镜像
 
 使用以下命令替换 gems 默认源:

```bash
# 添加 TUNA 源并移除默认源
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
# 列出已有源
gem sources -l
# 应该只有 TUNA 一个
```
或者，编辑 ~/.gemrc，将 https://mirrors.tuna.tsinghua.edu.cn/rubygems/ 加到 sources 字段。


参考： 
+ [gems.ruby-china.org](http://gems.ruby-china.org/)
+ [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/)
