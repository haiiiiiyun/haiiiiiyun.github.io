---
title: Django 项目的持续集成
date: 2016-08-18
writing-time: 2016-08-18 12:10--12:48
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

> Martin Fowler: http://martinfowler.com/articles/continuousIntegration.html
> 持续集成是一种软件开发实践。其中的团队成员频繁地集成他们的工作成果，通常是每人每天至少集成一次--从而形成了每天的多次集成。每次集成都由一个自动化创建过程验证，以便能尽快检测出集成错误。很多团队认为这种方式能有效减少集成问题。

使用持续集成时典型的开发流程：

1. 开发人员编写代码，在本地运行测试，再将代码提交到代码库。
1. 代码库通知自动化工具有关代码已提交待集成的信息。
1. 自动化工具将代码集成到项目中，并构建出一个新版本。构建过程中有任何错误，都将拒绝该次提交。
1. 自动化工具在新构建版本上运行开发人员写的测试。测试过程中有任何错误，都将拒绝该次提交。
1. 开发人员将收到成功或失败的详细信息。基于这些报告，可以进行相应修改。如果没有失败，表示本次集成成功。

# 持续集成的基本原则

## 编写大量测试

## 构建过程要尽量快

这很需要技巧。如果运行太慢，持续集成将不具优势，反而会成为负担。

提升大型项目测试速度的建议：

+ 避免使用 fixtures
+ 尽量避免使用 TransactionTestCase
+ 避免使用有大量操作的 setUp() 方法
+ 编写小型、专一任务的测试，然后加一些较大的集成式的测试
+ 学习如何为测试优化数据库。[参考 Stackoverflow.com](http://stackoverflow.com/a/9407940/93270)


# 集成测试的工具

## Tox

[Tox](http://tox.readthedocs.org/) 是一个通用的 virtualenv 管理和测试命令行工具。它使用一个命令就能完成项目针对不同版本的 Python 和 Django 的测试。当然也能针对不同的数据库引擎进行测试。现在都是用这个工具对代码与不同版本的 Python 的兼容性进行测试的。

相关功能：

+ 检查软件包能否在不同的 Python 版本上正确安装。在一个命令中就能完成对 Python 2.7, 3.4 和 PyPy 的检验
+ Tox 在每个环境下都运行一次测试
+ 它能作为 “持续集成服务器的前端，减少样板文件并且能合并 CI 和 Shell 中的测试”


## Jenkins

[Jenkins](http://jenkins-ci.org/) 是一个可扩展的持续集成引擎。它是自动化完成持续集成各部件的标准工具，具有一个很大的社区和生态系统。

# 提供持续集成的服务

有很多基于 Jenkins 等的自动化服务，并且大部分对开源项目都免费。

服务名        | 支持的 Python                  | 链接
--------------|--------------------------------|
Travis-CI     | 3.3, 3.2, 2.7, 2.6, PyPy       | https://travis-ci.org
AppVeyor(Win) | 3.4, 3.3, 2.7                  | http://www.appveyor.com
CircleCI      | 3.4, 3.3, 2.7, 2.6 PyPy 等其它 | https://circleci.com
Drone.io      | 2.7, 3.3                       | https://drone.io/
Codeship      | 3.4, 2.7                       | https://codeship.com


## 提供代码覆盖率的服务

codecov.io 能提供相关服务。

# 相关资料：

+ http://en.wikipedia.org/wiki/Continuous_Integration
+ http://jenkins-ci.org/
+ http://www.caktusgroup.com/blog/2010/03/08/django-and-hudson-ci-day-1/
+ http://ci.djangoproject.com/
+ http://docs.python-guide.org/en/latest/scenarios/ci/


 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
