---
title: 如何用 cookiecutter-django 进行 Django 项目布局
date: 2016-07-14
writing-time: 2016-07-14 09:27--10:34
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

以下介绍的是 [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) 项目布局模板。

其它类似的项目模板可以到 [这里](https://www.djangopackages.com/grids/g/cookiecutters/) 找到。

# Django 1.8 默认生成的布局

生成命令：

```
$ django-admin.py startproject mysite
$ cd mysite
$ django-admin.py startapp my_app
```

生成的布局：

```
mysite/
    manage.py
    my_app/
        __init__.py
        admin.py
        models.py
        tests.py
        views.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```


# cookiecutter-django 的项目布局

```
<repository_root>/
    <django_project_root>/
        <configuration_root>/
```

## 最顶层：仓库根目录 &lt;repository_root&gt;

**&lt;repository_root&gt;** 是项目所有文件的根目录，里面除了放置 **&lt;django_project_root&gt;** 以外，还放置其它的一些关键内容，如 *README.rst*, *docs/* 目录， *.gitignore*,  *requirements.txt* 文件及其它一些部署相关的文件等。

应该在该目录下运行 `django-admin.py startproject` 来创建 Django 项目（比如创建项目根目录 **&lt;django_project_root&gt;** ）

## 第二层：项目根目录 &lt;django_project_root&gt;

该目录是实际 Django 工程的根目录，所有的 Python 代码文件都放在 **&lt;django_project_root&gt;** 及其子目录下。

## 第三层：配置文件根目录 &lt;configuration_root&gt;

该目录包含 settings 模块和根 URLConf (urls.py)。该目录必须是一个有效的 Python 包（含 __init__.py 文件）。

配置文件根目录下的文件都是由 `django-admin.py startproject` 命令创建的。


# 项目布局举例

```
icecreamratings_project/
    .gitignore
    Makefile
    docs/
    README.rst
    requirements.txt
    icecreamratings/
        manage.py
        media/ # Development ONLY!
        products/
        profiles/
        ratings/
        static/
        templates/
        config/
            __init__.py
            settings/
            urls.py
            wsgi.py
```

其中， **icecreamratings_project** 就是 **&lt;repository_root&gt;**。

其它文件/目录描述如下：

文件或目录            | 目的
----------------------|
README.rst 和 docs/   | 项目文档
Makefile              | 包含一些简单的部署任务或宏，复杂的部署可以用 [Invoke](https://pypi.python.org/pypi/invoke)，[Paver](https://pypi.python.org/pypi/Paver) 和 [Fabric](http://fabfile.org) 
requirements.txt      | 项目的依赖包清单
icecreamratings/ 目录 | 对应 &lt;django_project_root&gt; 目录

在 **icecreamratings_project/icecreamratings/** 目录内，即 **&lt;django_project_root&gt;** 目录内，有以下的文件/目录：

文件或目录      | 目的
----------------|
manage.py       | Django 默认生成，不要修改它
media/          | 只用于开发环境：用户产生的静态文件，比如上传的照片等。大型项目会将静态文件分开单独部署
static/         | 非用户产生的静态文件，比如 CSS、JavaScript、图片等。大型项目会将静态文件分开单独部署
products/ 目录  | 一个 Django App 目录
profiles/ 目录  | 另一个 Django APP 目录
ratings/ 目录   | 另一个 Django APP 目录
templates/ 目录 | Django 项目级的模板目录


# 如何处理 Virtualenv ？

Virtualenv 目录不要和项目文件放在一起，应该统一放在独立的一个目录下。

所有的依赖文件信息都已写在 **requirements.txt**，因此无需将 Virtualenv 目录的内容加入版本控制管理。

比如对于该工程：

在 Mac OS X 和 Linux 上，对应的项目目录和 Virtualenv 目录可以为：

```
~/projects/icecreamratings_project/
~/.envs/icecreamratings/
```

在 Win 上，对应的项目目录和 Virtualenv 目录可以为：

```
c:\projects\icecreamratings_project\
c:\envs\icecreamratings\
```

如果使用使用 virtualenvwrapper (Mac OS X 或 Linux) 或 virtualenvwrapper-win (Windows)，那么 Virtualenv 的根目录会是 "~/.virtualenvs/"，而该项目对应的 Virtualenv 目录会是： `~/.virtualenvs/icecreamratings/`。


## 列出当前环境的所有依赖包：

```
$ pip freeze --local
```

# 通过 startproject 使用 cookiecutter 项目模板

[cookiecutter-django](https://github.com/pydanny/cookiecutter-django) 支持 Python 2.7+ 和 3.3+ 、Django 1.8 + 。

1. 安装 cookiecutter：

```
$ sudo apt-get install cookiecutter
```

2. 运行 cookiecutter，并指定模板路径，用来生成项目：

```
$ cookiecutter https://github.com/pydanny/cookiecutter-django
```

运行过程中会询问项目名称、数据库配置等相关的项目配置信息。

运行例子：

```
Cloning into 'cookiecutter-django'...
remote: Counting objects: 2358, done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 2358 (delta 4), reused 0 (delta 0), pack-reused 2346
Receiving objects: 100% (2358/2358), 461.95 KiB, done.
Resolving deltas: 100% (1346/1346), done.
project_name (default is "project_name")? icecreamratings
repo_name (default is "icecreamratings")? icecreamratings_project
author_name (default is "Your Name")? Daniel
and Audrey Roy Greenfeld
email (default is "audreyr@gmail.com")? hello@twoscoopspress.org
description (default is "A short description of the project.")? A website
for rating ice cream flavors and brands.
domain_name (default is "example.com")? icecreamratings.audreyr.com
version (default is "0.1.0")? 0.1.0
timezone (default is "UTC")? America/Los_Angeles
now (default is "2015/01/13")? 2015/05/18
year (default is "2015")?
use_whitenoise (default is "y")?
github_username (default is "audreyr")? twoscoops
full_name (default is "Audrey Roy")? Daniel and Audrey Roy Greenfeld
```

3. 进入生成的项目目录

`$ cd icecreamratings_project`

4. 创建 git 仓库

```
$ git init
$ git add .
$ git commit -m "first awesome commit"
$ git remote add origin git@github.com:somebody/icecreamratings.git
$ git push -u origin master
```

另忘记修改 README.rst 文件。

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
