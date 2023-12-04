---
title: Fabric 基础
date: 2017-01-13
writing-time: 2017-01-13 15:40-- 2017-01-14 17:02
categories: Tools
tags: Admin Python Fabric SSH
---

# Fabric 是什么

Fabric 即是一个 Python(2.5-2.7) 库，也是一个命令行工具，它能基于 SSH 完成应用部署和系统管理等任务。

更具体来说，它是：

+ 一个能让你通过命令行执行任意 Python 函数的工具。
+ 一个函数库（基于低层的库），能使基于 SSH 执行 shell 命令更加容易。


# Hello, fab

在当前工作目录下创建一个 `fabfile.py` 文件，在里面新建一个 `hello` 函数：

```python
def hello():
    print("Hello world!")
```

该函数可以在当前目录下通过 `fab hello` 执行。 `fab` 工具是在使用 `pip install fabric` 安装 fabric 时一并创建的。

```bash
$ fab hello
Hello world!

Done.
```

# 任务参数

通常我们需要将参数传入任务中，Fabric 的任务传参使用和 shell 兼容的记法： `<taskname>:<arg>,<kwarg>=<value>,...`。

对上面的 hello 进行扩展：

```python
def hello(name="world"):
    print("Hello %s!" % name)
```

调用如下：

```bash
$ fab hello  # 默认参数
Hello world!

Done.

$ fab hello:name=Jeff
Hello Jeff!

Done.

$ fab hello:Jeff
Hello Jeff!

Done.
```

要注意的是，这些参数都是以字符串类型传入的。


# 执行本地命令

假设我们有一个 Django Web 应用，该应用通过 git 部署到 `vcshost` 服务器。Web 应用的目录结构如下：

```
.
|-- __init__.py
|-- app.wsgi
|-- fabfile.py <-- our fabfile!
|-- manage.py
`-- my_app
    |-- __init__.py
    |-- models.py
    |-- templates
    |   `-- index.html
    |-- tests.py
    |-- urls.py
    `-- views.py
```

当在本地完成开发后，需要通过 fab 完成自动部署。

先进行测试，再进行 git 提交：

```python
from fabric.api import local

def prepare_deploy():
    local("python manage.py test my_app")
    local("git add -p && git commit")
    local("git push")
```

运行如下：


```bash
$ fab prepare_deploy
[localhost] run: ./manage.py test my_app
Creating test database...
Creating tables
Creating indexes
..........................................
----------------------------------------------------------------------
Ran 42 tests in 9.138s

OK
Destroying test database...

[localhost] run: git add -p && git commit

<interactive Git add / git commit edit message session>

[localhost] run: git push

<git push session, possibly merging conflicts interactively>

Done.
```

Fabric API 中的 `local`，可以用来运行本地的 shell 命令。

# 可任意组织代码

由于 fabfile.py 就是一个 Python 文件，因此里面的代码可以按你自己的风格进行组织。比如将任务分成多个子任务：

```python
from fabric.api import local

def test():
    local("python manage.py test my_app")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()
```

# 失败

Fabric 每次通过 local 运行本地程序后，都会对返回值进行检查，如果程序是非正常退出的，Fabric 会中止运行。例如，当 test 命令出错时：

```bash
$ fab prepare_deploy
[localhost] run: ./manage.py test my_app
Creating test database...
Creating tables
Creating indexes
.............E............................
======================================================================
ERROR: testSomething (my_project.my_app.tests.MainTests)
----------------------------------------------------------------------
Traceback (most recent call last):
[...]

----------------------------------------------------------------------
Ran 42 tests in 9.138s

FAILED (errors=1)
Destroying test database...

Fatal error: local() encountered an error (return code 2) while executing 'python manage.py test my_app'

Aborting.
```

## 失败处理

通过一个 [warn_only](http://docs.fabfile.org/en/1.13/usage/env.html#warn-only) 设置项（或环境变量，env var），能将默认中止的行为改为警告，如下：

```python
from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        result=local('python manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests faild. Continue anyway?")
        abort("Aborting at user request.")

[...]
```

解析如下：

+ `__future__` 导入命令将 `with` 指令加入 Python 2.5
+ Fabric 的 `contrib.console` 模块，包含一个 `confirm` 函数，用来进行 "yes/no" 提问
+ `settings` 上下文管理器，用于将设置项应用于特定的代码块
+ `local` 等用来运行其它程序的操作命令能返回一个结果对象，包含 `failed`, `return_code` 等信息
+ `abort` 函数用于手动中止运行


# 建立连接

下面的 `deploy()` 任务将在一个或多个远程服务器上运行，以确保服务器上的代码是最新的：


```python
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

def deploy():
    code_dir = '/srv/django/myproject'
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
```


+ `cd` 命令在远程服务器上切换目录， `with cd(..)` 使得 with 内的所有任务都在该目录下运行。而在本地切换目录的命令是 `lcd`。
+ `run` 在远程服务器上运行命令，对应的本地版本是 `local`。


执行 deploy:

```bash
$ fab deploy
No hosts found. Please specify (single) host string for connection: my_server
[my_server] run: git pull
[my_server] out: Already up-to-date.
[my_server] out:
[my_server] run: touch app.wsgi

Done.
```

由于没有事先在 fabfile 中指定任何服务器连接， Fabric 无法确定在哪些服务器运行命令。

定义连接使用类似 SSH 的主机字符形式 `user@host:port`，默认会使用你的本地用户名，因为在本例中我们只需指定主机名 my_server。


## 远程交互

`git pull` 只能在已经 clone 代码后运行，因此第一次部署时要运行 `git clone`:

```python
def deploy():
    code_dir = '/srv/django/myproject'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
```

在服务器上运行 `git clone` 等程序时，会要求密码等验证信息。Fabric 在运行中，会要求我们输入交互信息。例如，当运行 `fab deploy` 时，如下：

```bash
$ fab deploy
No hosts found. Please specify (single) host string for connection: my_server
[my_server] run: test -d /srv/django/myproject

Warning: run() encountered an error (return code 1) while executing 'test -d /srv/django/myproject'

[my_server] run: git clone user@vcshost:/path/to/repo/.git /srv/django/myproject
[my_server] out: Cloning into /srv/django/myproject...
[my_server] out: Password: <enter password>
[my_server] out: remote: Counting objects: 6698, done.
[my_server] out: remote: Compressing objects: 100% (2237/2237), done.
[my_server] out: remote: Total 6698 (delta 4633), reused 6414 (delta 4412)
[my_server] out: Receiving objects: 100% (6698/6698), 1.28 MiB, done.
[my_server] out: Resolving deltas: 100% (4633/4633), done.
[my_server] out:
[my_server] run: git pull
[my_server] out: Already up-to-date.
[my_server] out:
[my_server] run: touch app.wsgi

Done.
```

可以看到，其中的 `Password:` 提示行，就是远程服务器上的 `git` 调用引发的交互输入。

## 事先定义连接信息

[env](http://docs.fabfile.org/en/1.13/usage/env.html) 是一个全局的 dict 对象，它包含有许多 Fabric 的设置信息，实际上，上面的 `settings` 对象只是一个对 `env` 的简单封装对象。因此，可以将 fabfile 修改成：

```python
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['my_server']

def test():
	do_test_stuff()
```

当 `fab` 加载 fabfile 时，env 变量的内容将会被修改。由于 `env.hosts` 是一个列表，因此我们的任务可以在多个远程服务器上运行。


> 参考： 

+ [Fabric: Overview and Tutorial](http://docs.fabfile.org/en/1.13/tutorial.html)
