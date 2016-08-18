---
title: 部署 Django 项目
date: 2016-08-18
writing-time: 2016-08-17 09:54--2016-08-18 11:22
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 小项目使用单服务器

缺点：无法迅速扩展，不支持突发流量。

## 何时选择这种方式

+ 如果之前没有相关经验的。这种方式能让你深入理解 Python Web 应用的工作原理。
+ 如果你的项目是实验性或试着玩的。
+ 如果你确信单台服务器性能足够。

## 示例： Ubuntu + Guniorn 快速设置

组件：

+ 一台旧电脑或便宜的云服务器
+ Ubuntu Server OS
+ PostgreSQL
+ Virtualenv
+ Gunicorn

用 apt-get 安装相关的工具：

pip/virtualenv: python-pip, python-virtualenv
PostgreSQ: postgresql, postgresql-contrib, libpq-dev, python-dev

其它的程序和包（比如 Django 和 Gunicorn 等），能用 pip 安装的都用 pip 安装。

之后，运行 `gunicorn myproject.wsgi` ，即可在浏览器中通过服务器的 IP 地址访问了。

# 中大型项目用多台服务器

企业或发展中的创业公司如果不选用 PaaS，一般会用多服务器配置。

基本的多服务器配置：

![Django 基本的多服务器配置]({{site.url}}/assets/images/django-basic-multi-server-setup.png)

+ 数据库服务器：如 PostgreSQL 和 MySQL
+ WSGI 应用服务器： 如 uWSGI，Gunicorn + Nginx, Apache + mod_wsgi

另外，可能还需要：

+ 静态文件服务器： 自己的服务器可以用 Nginx 或 Apache。但是 CDN (如 Amazon CloudFront) 可能更经济
+ 缓存/异步消息队列服务器：如 Redis，Memcached 或 Varnish
+ 其它服务器： 其它的 CPU 密集型任务，或者涉及等待外部接口的任务可以从 WSGI 应用服务器上分流出去


所有的临时数据都用 Redis 保存

Redis 和 Memcached 类似，但它还有以下的功能：

+ 认证功能
+ 能保持状态，因此服务器重启后能恢复数据
+ 额外的数据类型使其能作为异步消息队列使用（可以和 **celery** 和 **rq** 一起使用）

最后，还需要对每台服务器上的进程进行管理，推荐用：

+ Supervisord
+ initscripts

## 高级的多服务器设置

![Django 高级多服务器配置]({{site.url}}/assets/images/django-advanced-multi-server-setup.png)

负载均衡设备即可以是硬件也可以是软件。

+ 基于软件的： HAProxy, Varnish, Nginx
+ 基于硬件的： Foundry，Juniper，DNS load balancer
+ 基于云的： Amazon Elastic Load Balancer，Rackspace Cloud Load Balancer

## 水平和垂直扩展

水平扩展是增加多台服务器来分流负载。而垂直扩展是对现有服务器硬件进行升级，如加内存等。因此，垂直扩展更加容易。

## 水平扩展和会话数据

如上传文件时访问的是 server1，但是后来返回时，通过负载均衡器，访问的是 server2。解决这个问题的一般方法是将上传的数据保存到一个共享的驱动器中或到云服务器中（如 Amazon S3)

# WSGI 应用服务器

Django 项目一定要用 WSGI 部署。

Django 1.8 的 *startproject* 默认生成的 **wsgi.py** 文件中包含了能将 Django 项目部署到任何 WSGI 服务器的配置内容。

最常用的 WSGI 部署设置：

+ uWSGI + Nginx
+ Gunicorn 置于 Nginx 代理后
+ Apache + mode_wsgi

设置               | 优点                                                     | 缺点
-------------------|----------------------------------------------------------|
uWSGI + Nginx      | 有大量的功能和选项。配置非常灵活。据说性能比其它的都好。 | 文件还在完善。使用时间比 Apache 少。相比较对新手不太友好
Gunicorn (+ Nginx) | 用纯 Python 实现。                                       | 文档少
Apache + mod_wsgi  | 非常稳定，文档相当多                                     | 无法使用环境变量，Apahce 配置可能很复杂


# 性能优化： uWSGI 和 Gunicorn

这两者都能最大化服务的性能，且配置都很灵活。

资料：
+ http://uwsgi-docs.readthedocs.org
+ https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/uwsgi/
+ [Nginx+UWSGI](http://justcramer.com/2013/06/27/serving-python-web-applications/)
+ http://gunicorn.org/
+ http://cerebralmanifest.com/uwsgi-vs-gunicorn/

# 稳定性和易设置性： Gunicorn 和 Apache

能快速配置和上线应用。

# Apache 凝难杂症

## 不要使用 mod_python

Django 1.3 后就已去除了对 mod_python 的支持，现在用 mod_wsgi。

## Apache 和 环境变量

Apache 不支持环境变量。因此需要将保密值先放在 .ini、.cfg、.json、.xml 文件中然后再导入配置文件中。

## Apache 和 Virtualenv

Apache 和 virtualenv 很容易使用：

+ 如果使用 mod_wsgi 3.4 或更新版本，并且使用 daemon 模式，只需在 **WSGIDaemonProcess** 指令下添加： **python-home:/some/path/to/root/of/virtualenv**
+ 如果使用 embded 模式： **WSGIPythonHome /some/path/to/root/of/virtualenv**
+ 如果使用 mod_wsgi 3.3 或更老版本，并且使用 daemon 模式，在 **WSGIDaemonProcess** 下设置 **python-path=/some/path/to/root/of/virtual/lib/pythonX.Y**


# 自动化的可重复部署过程

服务器的配置应该自动化并且注明文档。

+ 应该能通过一个命令就可配置一台全新的服务器。
+ 这个命令应该有准确的文档描述。
+ 运行该命令时，应该不与现存的服务器存在依赖关系。
+ 任何一个脚本都应该是幂等的，无论它们运行多少次。


## 一个快速变换的世界

日期         | 配置管理工具
-------------|
直到 2011 年 | Chef/Puppet
2012 年      | 最好的是 Chef/Puppet,Salt/Ansible 还在开发
2013 年 1 月 | Chef/Puppet 还很强, Salt/Ansible 正变得流行
2013 年 5 月 | Docker 开源
2014 年 1 月 | Salt/Ansible 变得稳定和流行，Chef/Puppet 不再流行，Docker 还在开发
2015 年 5 月 | Docker 变得流行，Salt/Ansible 还在变强，Chef/Puppet 快速衰亡
2016 年      | Docker 成熟？

变换配置管理工具是很麻烦的，故谨慎选择工具。

# 该用哪个自动化工具？

## 自己研究

唯一的办法是自己试用每一个工具。

## 当前流行的自动化工具

Docker, Ansible, SaltStack, Puppet 和 Chef 都很流行。由于这些工具意在管理多台主机，因此都变得越来越复杂。

这些工具具有的功能：

**远程执行**

+ 在远程服务器上安装程序
+ 在远程服务器上运行命令
+ 在远程服务器上开启服务
+ 当命令在远程执行时，将日志和应答返回本地


**配置管理**

+ 创建或更新服务器上的 conf 文件。如为一个新安装的 PostgreSQL 实例创建 pg_hba.conf 文件
+ 为不同的服务器设置不同的配置值，如基于服务器 IP 或 OS 相关信息进行配置


业务流程和目标：

+ 控制任务将发给哪台服务器，何时发送
+ 管理不同组件，创建管道用于处理不同的工作流
+ 从主服务器上将任务推送到其它服务器，用 'push mode'
+ 询问主服务器需要实现什么， 有 'pull mode'


以上工具都能完成列出的这些功能，它们的区别有：

工具      | 优点                                                                                                        | 缺点
----------|-------------------------------------------------------------------------------------------------------------|
Docker    | 由于只需关注变动的部分，故部署很快。容器方式。YAML 配置。社区大。开源。                                     | 用 Go 编写。还在开发。
SaltStack | 主要是推送模式。用 Omq 传送非常快。YAML 配置。网上有大量示例。社区大。开源。用 Python 实现。             | 可能会变得非常复杂。还不够成熟。
Ansible   | 主要是推送模式。远程服务器上除了 OpenSSH，无需运行其它后台程序。易于学习。YAML 配置。开源。用 Python 实现。 | 用 SSH 传输较慢，但通用 Fireball 模式可以临时设置一个 Omq 后台进程。还不够成熟。
Chef      | 大量的示例。社区大。开源。                                                                                  | 非常难学。用 Ruby 实现。非常复杂。
Puppet    | 社区大。开源。                                                                                              | 非常难学。用 Ruby 实现。配置文件用自定义的 DSL 编写，很难用。


**关于 Fabric 和 Invoke**

它们只关注实现在远程执行命令。常和上面提到的这些工具一起使用。

现在的趋势是使用 Docket, SaltStack 和 Ansible。

# 其它资源

+ https://highperformancedjango.com
+ http://www.fullstackpython.com/deployment.html


 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
