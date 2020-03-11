---
title: Ubuntu 系统上 Python 项目开发本地虚拟环境管理方案： pyenv + pipenv
date: 2020-03-11
writing-time: 2020-03-11
categories: python;ubuntu
tags: python;ubuntu
---

# 1. 概述

本文介绍用 Pyenv + Pipenv 管理 Python 项目开发的本地虚拟环境。

+ pyenv: 安装和管理多个 Python 版本。
+ pipenv: 为每个项目创建独立的虚拟环境。

以下所有操作在 Ubuntu 16.04 系统上进行。

# 2. Python 版本管理: pyenv

## 2.1. 安装 pyenv

```bash
$ curl https://pyenv.run | bash
```

pyenv 相关的内容会安装在 `~/.pyenv/` 目录下。

安装后根据提示将以下内容添加到 `~/.bashrc`:

```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
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

安装 python 前，可能要先安装编译 python 所需的依赖包:

```bash
$ sudo apt-get install libc6-dev gcc
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
```

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

# 3. 虚拟环境管理: pipenv


## 3.1. 安装 pipenv

确保安装了最新的 3.x 版本 python 和 pip

```bash
$ python -V
Python 3.8.2

$ pip -V
pip 19.2.3 from /home/hy/.pyenv/versions/3.8.2/lib/python3.8/site-packages/pip (python 3.8)
```

安装：

```bash
$ pip install pipenv
```

升级：

```bash
$ pip install --upgrade pipenv
```

## 3.2. 为每个项目创建独立的虚拟环境

创建项目目录:

```bash
$ mkdir django_test && cd django_test
```

将 `export PIPENV_VENV_IN_PROJECT=1` 添加到 `~/.bashrc`，要想使配置生效，执行下 `source ~/.bashrc`, 之后 pipenv 管理的虚拟环境都会安装在项目根目录下的 `.venv` 目录中。

创建虚拟环境:

```bash
$ pipenv --python 3.8

Creating a virtualenv for this project…
Pipfile: /home/hy/workspace/temp/django_test/Pipfile
Using /home/hy/.pyenv/versions/3.8.2/bin/python (3.8.2) to create virtualenv…
⠸ Creating virtual environment...created virtual environment CPython3.8.2.final.0-64 in 178ms
  creator CPython3Posix(dest=/home/hy/workspace/temp/django_test/.venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/hy/.local/share/virtualenv/seed-app-data/v1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

✔ Successfully created virtual environment! 
Virtualenv location: /home/hy/workspace/temp/django_test/.venv
Creating a Pipfile for this project…

$ ls -la
total 16
drwxrwxr-x  3 hy hy 4096 3月  11 12:15 .
drwxrwxr-x 42 hy hy 4096 3月  10 13:02 ..
-rw-rw-r--  1 hy hy  138 3月  11 12:15 Pipfile
drwxrwxr-x  4 hy hy 4096 3月  11 12:15 .venv
```

其中自动生成的 `Pipfile` 生成中保存了 pypi 源的 URL：

```conf
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.8"
```

可以将源 URL 设置为国内的镜像地址来提高下载速度：

```conf
[[source]]
name = "pypi"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.8"
```

安装依赖包：

```bash
$ pipenv install "django==2.1"
Installing django==2.1…
Adding django to Pipfile's [packages]…
✔ Installation Succeeded 
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
✔ Success! 
Updated Pipfile.lock (a5a621)!
Installing dependencies from Pipfile.lock (a5a621)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 2/2 — 00:00:01
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

安装测试环境下的依赖包:

```bash
$ pipenv install pytest --dev
```

显示已安装的依赖包关系：

```bash
$ pipenv graph
Django==2.1
  - pytz [required: Any, installed: 2019.3]
pytest==5.3.5
  - attrs [required: >=17.4.0, installed: 19.3.0]
  - more-itertools [required: >=4.0.0, installed: 8.2.0]
  - packaging [required: Any, installed: 20.3]
    - pyparsing [required: >=2.0.2, installed: 2.4.6]
    - six [required: Any, installed: 1.14.0]
  - pluggy [required: >=0.12,<1.0, installed: 0.13.1]
  - py [required: >=1.5.0, installed: 1.8.1]
  - wcwidth [required: Any, installed: 0.1.8]
```


删除依赖包：


```bash
$ pipenv uninstall django
Uninstalling django…
Found existing installation: Django 2.1
Uninstalling Django-2.1:
  Successfully uninstalled Django-2.1

Removing django from Pipfile…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (91e3b9)!
```

进入虚拟环境：

```bash
$ pipenv shell
```

# 4. 项目管理

```bash
$ ls -la
total 20
drwxrwxr-x  3 hy hy 4096 3月  11 12:31 .
drwxrwxr-x 42 hy hy 4096 3月  10 13:02 ..
-rw-rw-r--  1 hy hy  185 3月  11 12:31 Pipfile
-rw-r--r--  1 hy hy 3666 3月  11 12:31 Pipfile.lock
drwxrwxr-x  5 hy hy 4096 3月  11 12:21 .venv
```

将自动生成的 `Pipfile` 和 `Pipfile.lock` 文件加入版本控制系统，`.venv` 目录不要加入版本控制系统。

团队成员安装好 pyenv 和 pipenv，在 `~/.bashrc` 中配置相应环境变量，clone 项目源码，运行 `pipenv install --dev` 即可重建虚拟开发环境。

```bash
$ cd django_test
$ pipenv install --dev
```

# 资源

+ [Ubuntu下安装pyenv实现Python多版本共存](https://www.linuxidc.com/Linux/2018-04/151988.htm)
+ [pyenv 官网](https://github.com/pyenv/pyenv)
+ [pipenv 文档](https://pipenv.pypa.io/en/latest/)
+ [利用pipenv和pyenv管理多个相互独立的Python虚拟开发环境](https://blog.csdn.net/liuchunming033/article/details/79582617)
