---
title: 理想的 Django 环境设置
date: 2016-07-13
writing-time: 2016-07-13 14:57
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 在开发、测试和生产等所有环境中都使用相同的数据库引擎

使用的数据库不相同，会有以下问题：

1. 无法将生产环境中取得的数据原封不动地还原到本地进行测试
2. 不同的数据库有不同的类型/限制，Django 的 ORM 不可以做到十全十美
3. 不能依赖 `fixtures` 来消除本地和生产环境间的数据库差异， `fixtures` 只能用于创建简单的硬编码的测试数据，不能作为数据库无关的数据插入工具

Django 项目一般使用 PostgreSQL，安装 PostgreSQL:

+ Mac: 下载这个[一键安装程序](http://postgresapp.com)
+ Windows: 下载这个[一键安装程序](http://postgresql.org/download/windows/)
+ Linux: 通过包管理器安装，或者按[该文档](http://postgresql.org/download/linux/) 进行

# 使用 Pip 和 Virtualenv

Python 3.4 及以上版本已经默认包含了 Pip，安装方法：

+ pip: [http://pip-installer.org](http://pip-installer.org)

+ virtualenv: [http://virtualenv.org](http://virtualenv.org)

由于 virtualenv 比较难用，推荐在 virtualenv 的基础上安装使用 virtualenvwrapper：

+ 对于 Mac OS X 和 Linux: [virtualenvwrapper](http://virtualenvwrapper.rtfd.org)
+ 对于 Win: [virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win)

# 通过 pip 来安装 Django 及其它依赖包

每个 Django 项目都应有一个 `requirements.txt` 文件，指定依赖的包名及其版本。

## 设置 PYTHONPATH

将你的项目根目录添加到其 Virtualenv 的 PYTHONPATH 中，在项目根目录下运行 `pip install -e .` 即可。

更多文献：

+ [http://cs.simons-rock.edu/python/pythonpath.html](http://cs.simons-rock.edu/python/pythonpath.html)

+ [https://docs.djangoproject.com/en/1.8/ref/django-admin/](https://docs.djangoproject.com/en/1.8/ref/django-admin/)


# 使用版本控制系统

最流行的工具有 **Git** 和 **Mercurial** 。

托管服务有 [github](https://github.com) 和 [bitbucket](https://bitbucket.org)。

# 使用相同的环境

要消除以下几种环境差异：

1. 操作系统差异： 如在 Mac 和 Win 上开发，在 Ubuntu 上部署
2. Python 设置的差异: 如使用不同的版本
3. 开发者之间的差异

## 使用 Vagrant 和 VirtualBox 来设置统一的开发环境

例如，如果你使用 Mac，但项目部署环境是 Ubuntu，则可以在 Mac 上通过使用 Vagrant 及项目中的 Vagrantfile 来快速产生一个配置好了的虚拟 Ubuntu 开发环境。

优点：
1. 项目开发团队中的每个人都能获取完全相同的本地开发环境
2. 测试和生产环境可以用和本地开发环境类似的方式进行配置

缺点：
1. 对于小项目来说，提高了复杂度
2. 在旧机器上，运行虚拟机会比较慢


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
