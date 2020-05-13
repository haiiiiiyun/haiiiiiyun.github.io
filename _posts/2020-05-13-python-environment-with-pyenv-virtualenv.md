---
title: Ubuntu 系统上 Python 项目开发本地虚拟环境管理方案： pyenv + virtualenv
date: 2020-05-13
writing-time: 2020-05-13
categories: python.ubuntu
tags: python ubuntu
---

# 1. 概述

由于使用 pipenv 安装相关包时非常慢，特别是 Lock 操作，故不推荐使用。

本文介绍用 Pyenv + virtualenv 管理 Python 项目开发的本地虚拟环境。

+ pyenv: 安装和管理多个 Python 版本。
+ virtualenv: 为每个项目创建独立的虚拟环境。

以下所有操作在 Ubuntu 16.04 系统上进行。

# 2. Python 版本管理: pyenv

## 2.1. 安装 pyenv

```bash
$ curl https://pyenv.run | bash
```

pyenv 相关的内容会安装在 `~/.pyenv/` 目录下。

安装后根据提示将以下内容添加到 `~/.bashrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
```

升级 pyenv:

```bash
$ pyenv update
```

删除 pyenv:

```bash
$ rm -rf ~/.pyenv
```

并删除 ~/.bashrc 中的相关环境变量。


## 2.2. 安装和管理多个 Python

查看可安装的版本：

```bash
$ pyenv install --list
```

安装指定版本:

```bash
$ pyenv install 3.8.2
```

安装 python 前，要先安装编译 python 所需的依赖包:

```bash
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

见 [Common build problems](https://github.com/pyenv/pyenv/wiki/Common-build-problems), 不然编译后导入某些 python 库时会出现 `ModuleNotFoundError: No module named '_sqlite3'` 等问题。

查看当前已安装的 python 版本:

```bash
$ pyenv versions
* system (set by /home/hy/.pyenv/version)
  3.8.2
```

通过 pyenv 安装的所有 Python 版本都保存在 `~/.pyenv/versions/` 目录下。


## 2.3. 每个目录可指定执行特定的 Python 版本

没有指定前，系统默认的 Python 为 2.7:

```bash
$ mkdir test
$ cd test
$ python
Python 2.7.12 (default, Oct  8 2019, 14:14:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

通过 `pyenv local` 命令指定，当在该目录下执行 python 时，执行的 python 版本：

```bash
$ pyenv local 3.8.2

$ ls -la
total 12
drwxrwxr-x  2 hy hy 4096 3月  10 16:04 .
drwxrwxr-x 42 hy hy 4096 3月  10 13:02 ..
-rw-rw-r--  1 hy hy    6 3月  10 16:03 .python-version

$ cat .python-version 
3.8.2
```

`local` 命令会在当前目录下生成一个包含版本号的隐藏文件 `.python-version`。


验证执行的 python 版本:

```bash
$ python
Python 3.8.2 (default, Mar 10 2020, 13:47:49) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```


## 2.4. 切换全局 Python 版本

```bash
$ pyenv global 3.8.2

$ python
Python 3.8.2 (default, Mar 10 2020, 13:47:49) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

# 3. 虚拟环境管理: pyenv-virtualenv


## 3.1. 安装 pyenv-virtualenv

```bash
$ git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
$ source ~/.bashrc
```

## 3.2. 创建独立的虚拟环境

创建项目目录:

```bash
$ pyenv virtualenv 3.8.2 py38
```

该命令为 python 3.8.2 创建一个名为 py38 的虚拟环境，保存在 `~/.pyenv/versions/` 下：

```bash
$ pyenv versions

  system
  *3.8.2
  3.8.2/envs/py38
  py38
```

切换和使用 python 虚拟环境：

```bash
$ pyenv activate py38
$ pip install django

$ pyenv deactivate
```

删除虚拟环境：

```bash
$ pyenv uninstall py38 # or
#$ rm -rf ~/.pyenv/versions/py38/
```

为切换虚拟环境命令设置 alias:

```bash
$ echo 'workon="pyenv activate "' >> ~/.bashrc
$ ~/.bashrc

$ workon py38
```

.bashrc 中的相关设置为：

```bash
# pyenv & virtualenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
alias workon='pyenv activate '
```

# 4. Mac 上的设置

和 Ubuntu 上的操作类似，但相关设置保存在 ~/.~/.bash_profile 中，不要放在 ~/.bashrc 中即可。

# 资源

+ [Ubuntu下安装pyenv实现Python多版本共存](https://www.linuxidc.com/Linux/2018-04/151988.htm)
+ [pyenv 官网](https://github.com/pyenv/pyenv)
+ [pyenv Common build problems](https://github.com/pyenv/pyenv/wiki/Common-build-problems)
+ [python实现多版本环境pyenv、virtualenv、virtualenvwrapper](https://blog.csdn.net/qq_42672770/article/details/100185090)
