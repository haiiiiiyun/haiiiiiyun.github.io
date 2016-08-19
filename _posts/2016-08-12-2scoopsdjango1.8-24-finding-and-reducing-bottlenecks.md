---
title: 查找 Django 项目中的性能瓶颈
date: 2016-08-12
writing-time: 2016-08-11 14:17--2016-08-12 09:52
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 需要考虑该问题吗？

过早地优化是不好地！对于中小型的网站，一般不必考虑。

# 针对查询操作较多的页面进行优化提速

推荐看 [Django 官方的数据库优化文档](https://docs.djangoproject.com/en/1.8/topics/db/optimization/)

## 通过 django-debug-toolbar 分析查询操作

该工具能检测出查询操作都来自何处。从而能检测出到以下瓶颈：

+ 页面中的重复查询
+ ORM 调用引起的查询操作次数比预想的多
+ 查询很慢

先在本地安装 django-debug-toolbar，在浏览器中打开要检查的页面，然后展开 SQL 面板，从中就能看到当前页包含的所有查询操作了。

性能分析的相关包：

+ django-debug-toolbar: 对于逐页分析很有用。推荐将 django-cache-panel 加入项目中，从而在开发时能检查 cache
+ django-extensions: 它带有一个工具叫 RunProfileServer，它开启的 Django server 具有 hotshot/profiling 等功能。
+ silk: [Silk](https://github.com/mtford90/silk) 是一个实时地 Django 性能分析应用，它在显示结果前就将 HTTP 请求和数据库查询操作进行劫持和存储，以便进行后续分析。

## 减少查询次数的方法

+ 尝试在 ORM 中使用 select_related() 来组合查询操作。它能顺着 ForeignKey 链将多个查询组合成一个大查询。如果使用 CBV，django-braces 提供了 SelectRelatedMixin。通过明确地传入用到的项名来避免查询数据过大。
+ 由于 M2M 和 M2O 关系无法用 select_related() 优化，考虑使用 prefetch_related()
+ 如果模板中多次进行了相同的查询操作，应将查询移到 Python 视图中，并将该 ORM 调用作为一个上下文变量，然后在模板中使用该变量进行查询操作
+ 使用 Memcached 等键/值对存储器实现缓存，然后编写测试来确认视图中的查询次数（[assertNumQueries()](https://docs.djangoproject.com/en/1.8/topics/testing/tools/) ）。
+ 使用 **django.utils.functional.cached_property** 装饰器将方法调用结果缓存到内存中，其有效时间是方法所属对象实例的生命期。这种方法相当有用

## 提升普通的查询操作

+ 确保你的索引对大多数的慢查询操作有帮助。检查这些查询生成的原始 SQL 语句，对经常进行过滤/排序的项进行索引。检查生成的 WHERE 和 ORDER_BY 子句
+ 理解索引在生产环境中的实际功用。开发机上不可能完全重现生产环境下的问题
+ 打开数据库上的慢查询日志功能，检查这些慢查询是否经常出现
+ 在开发机上打开 django-debug-toolbar 进行调试

一旦进行了正确的索引，并且进行了充分的分析后，在重构时要考虑：

+ 重写逻辑，使返回的数据集尽可以小
+ 重构数据模型，使索引能更加有效工作
+ 如果 ORM 生成的语句效率不高，可以使用原始 SQL


### 如果对原始 SQL 查询进行分析 ：

+ Postgresql： 参考 [postgresql-performance](http://www.revsys.com/writings/postgresql-performance.html) 和 [more on postgres performance](http://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/)
+ MySQL : 参考  [explain](http://dev.mysql.com/doc/refman/5.6/en/explain.html)
+ django-debug-toolbar 的 SQL 面板上有 EXPLAIN 功能

## 将 ATOMIC_REQUESTS 改为 False

但是通常来说，将所有查询放在事务中而导致的性能损失并不太明显。

# 最大化利用数据库功能

## 了解哪些东西不能存放在数据库中

Frank Wiles 说有 3 样东西千万不要存放到关系型数据库中：

1. 日志。可以使用第三方服务如 Splunk、 Loggly 或 NoSQL 数据库
1. 临时数据。如 django.contrib.sessions 和 django.contrib.messages 等，可以用 Memcached、Redis、Riak 和 NoSQL
1. 二进制数据。如 django.db.models.FielField。可使用 AWS CloudFront 或 S3

## 充分利用 PostgreSQL

参数资料：

+ http://wiki.postgresql.org/wiki/Detailed_installation_guides
+ http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server
+ http://www.revsys.com/writings/postgresql-performance.html
+ http://2scoops.co/craig-postgresql-perf
+ http://2scoops.co/craig-postgresql-perf2
+ [PostgreSQL 9.0 High Performance](http://amzn.to/1fWctM2)

## 充分利用 MySQL

[High Performance MySQL](http://amzn.to/188VPcL)

# 使用 Memcached 或 Redis 对查询进行缓存

参考资料：

+ https://docs.djangoproject.com/en/1.8/topics/cache/
+ https://github.com/sebleier/django-redis-cache/

# 决定对哪些部分进行缓存

+ 哪些视图/模板包含最多的查询
+ 哪些 URL 访问最多
+ 缓存何时失效

# 考虑使用第三方缓存包

它们有额外的特性：

+ 能缓存查询集
+ 缓存失效的设置/机制
+ 不同的缓存后端
+ 不同的缓存方式

较常用的包：

+ django-cache-machine
+ johnny-cache

# 压缩 HTML、CSS 和 JavaScript

Django 的工具有：  GzipMiddleware 和 {% raw %}{%spaceless%}{% endraw %} 模板 Tag。

使用 Django 和 Python 进行处理会影响性能，更好的方法是通过 Apache、Nginx 等服务器来对输出内容进行压缩。而一种折中的方式是使用第三方库对 CSS 和 JavaScript 进行预先压缩。推荐使用 django-pipeline。

# 使用上游缓存或 CDN

上游缓存有 [Varnish](http://varnish-cache.org/)。

# 其它资源

## 关于 Web 性能的常用最佳实践：
+ [YSlow’s Web Performance Best Practices and Rules](http://developer.yahoo.com/yslow/)
+ [Google’s Web Performance Best Practices](https://developers.google.com/speed/docs/best-practices/rules_intr)

# 关于扩展大型 Django 网站：
+ [Written with a focus on scaling Django](https://highperformancedjango.com)
+ [David Cramer often writes and speaks about scaling Django at Disqus, Dropbox, and Sentry](http://justcramer.com/)


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
