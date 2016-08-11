---
title: 查找性能瓶颈
date: 2016-08-11
writing-time: 2016-08-11 14:17
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 需要考虑该问题吗？

过早地优化是不好地！对于中小型的网站，一般不必考虑。

# 针对查询操作较多的页面进行优化提速

推荐看 [Django 官方的数据库优化文档](https://docs.djangoproject.com/en/1.8/topics/db/optimization/)

## 通过 django-debug-toolbar 分析查询操作

该工具能检测出这些查询操作都来自何处。从而查到以下的瓶颈：

+ 页面中重复地查询
+ ORM 调用引起的查询操作次数比预想的多
+ 查询很慢

先在本地安装 django-debug-toolbar，在浏览器中打开要检查的页面，然后展开 SQL 面板，从中就能看到当前页包含的所有查询操作了。

性能分析的相关包：

+ django-debug-toolbar: 对于逐页分析很有用。推荐将 django-cache-panel 加入项目中，从而在开发时能检查 cache
+ django-extensions: 它带有一个工具叫 RunProfileServer，它开启的 Django server 具有 hotshot/profiling 等功能。
+ silk: [Silk](https://github.com/mtford90/silk) 是一个实时地 Django 性能分析应用，它在显示结果前就将 HTTP 请求和数据库查询操作进行劫持和存储，以便后续的分析。

## 减少查询次数的方法

+ 尝试在 ORM 中使用 select_related() 来组合查询操作。它能顺着 ForeignKey 链将多个查询组合成一个大的查询中。如果使用 CBV，django-braces 提供了 SelectRelatedMixin。通过明确地传入用到的项名来避免查询数据过大。
+ 由于 M2M 和 M2O 关系无法用 select_related() 优化，考虑使用 prefetch_related()






















> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
