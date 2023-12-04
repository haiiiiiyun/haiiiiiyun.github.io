---
title: Django 中的异步任务队列
date: 2016-08-12
writing-time: 2016-08-12 10:00--11:38
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

涉及的三个概念：

+ 代理：指任务存储器本身。Django 中一般用 RabbitMQ 和 Redis。
+ 生产者：将任务添加到队列的那些代码。指应用代码。
+ 工作者：将任务从代理时取出并执行的那些代码。通常有多个工作者，它们在后台同时运行。

# 是否需要任务队列？

+ 需要长时间处理才能得到的结果：应该用
+ 用户能够并且应该立即看到的结果：不应该用

要使用任务队列吗？ | 任务
-------------------|
要                 | 发送批量邮件
要                 | 修改文件（包括图片）
要                 | 通过第三方 API 获取大量数据
要                 | 插入或更新大量记录到数据表中
不                 | 更新用户资料
不                 | 添加一篇文章
要                 | 进行非常费时的计算
要                 | 发送或接收 Webhooks

不过同时还要考虑网站的规模：

+ 对于中小流量的网站，可以完全不必使用任务队列
+ 而大流量的网站，可能每个操作都需要任务队列

# 选择任务队列软件

软件                    | 优点                                                                     | 缺点
------------------------|--------------------------------------------------------------------------|
Celery                  | 事实上的 Django 标准，支持不同的存储类似，灵活、功能齐全、适合高流量网站 | 配置复杂，对小流量网站来说是杀鸡用牛刀
Redis Queue             | 灵活、比 Celery 使用的内存少，适合高流量网站                           | 功能没有 Celery 强大，配置难度中等，只支持 Redis 存储
django-background-tasks | 非常易配置、易用，适合小型网站和批处理任务，使用 Django ORM 作为后端     | 因使用 Django ORM 为后端，非常不适合用于中高流量的网站

# 任务队列最佳实践

## 把任务当作视图对待

任务中包含的代码要尽量少，代码和视图一样，尽量放在辅助模块和函数中。因所有的任务队列软件都会对我们的任务函数进行序列化/抽象化，将实现代码放在函数中更加易于调试和复用。

## 任务不是免费的

虽然在后台运行，但是还是要消耗资源。

## 对任务函数只传递能进行 JSON 序列化的值

这将参数类型限制为：整数、浮点数、字符串、列表、元组和字典。

不传递复杂对象的原因：

+ 传入一个对象持久化数据（如 ORM 实例）可能在任务还没有开始时就已失效，而传入主键就能获取最新数据
+ 传入复杂对象在进行序列化时费时费力
+ 更易调试
+ 有些任务队列只支持 JSON 序列化值

## 学习如果监控任务和工作者

+ [Celery](https://pypi.python.org/pypi/flower)
+ [Redis Queue](https://pypi.python.org/pypi/django-redisboard)
+ [使用 django-rq 的 Redis Queue](https://pypi.python.org/pypi/django-rq)
+ django-background-tasks: django.contrib.admin

## 日志

由于任务在后台运行，最好在每个任务函数中进行日志记录。

## 监测积压项

随着流量增加，任务会增加，而工作者如果没有相应增加，任务最会积压。此时可考虑升级任务队列软件。

## 周期性地清除已僵死的任务

## 忽略不需要的返回结果

## 使用队列的错误处理机制

+ 某个任务的最多重试次数
+ 重试间隔时间

应着重考虑重试间隔时间，一般任务失败后，至少等待 10 秒后再重试。

## 充分挖掘所选任务队列软件的功能

# 相关资源

## 通用

+ http://www.fullstackpython.com/task-queues.html
+ http://www.2scoops.co/why-task-queues/  幻灯片
+ https://pypi.python.org/pypi/django-transaction-hooks

## Celery

+ [Celery 官网](http://celeryproject.com)
+ [学习 Celery 必读](https://denibertovic.com/posts/celery-best-practices/)
+ [一个管理 Celery 蔟的 Web 工具](https://pypi.python.org/pypi/flower)
+ http://wiredcraft.com/blog/3-gotchas-for-celery/
+ https://www.caktusgroup.com/blog/2014/06/23/scheduling-tasks-celery/

## Redis-Queue
+ [Redis Queue 官网](http://python-rq.org/)
+ http://racingtadpole.com/blog/redis-queue-with-django/

## django-background-tasks

+ https://pypi.python.org/pypi/django-background-tasks


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
