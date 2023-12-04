---
title: Django App 设计基本原则
date: 2016-07-14
writing-time: 2016-07-14 10:51--11:27
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 基本原则

每个 App 都应该只做一件事。它的功能应该能用一句简单的语句就可以描述清楚，如果描述过程中用了一个以上的 ”以及“，可能就意味着这个 App 有点大了，需要拆分。

> James Bennett:
> The art of creating and maintaining a good Django app is that it should follow the truncated Unix philosophy according to Douglas McIlroy: 'Write programs that do one thing and do it well.'


# 如何命名 Django App

1. 尽量用一个单词， 如 **animals**, **blog**, **dreams**， **polls**。简单且语义明晰的项目名更易维护。

2. 如果合适，可以参考该 App 内主数据模型的名称，App 名用其复数形式。

3. 命名时考虑 URL 的形式，比如 blog 的 URL 可以会是 http://www.example.com/weblog/，那么可以考虑把 App 命名为 weblog，而不是 blog 或者 posts。

4. 命名用全小字的字母，不要用数字等其它字符，如果需要，可以用下划线 `_`，但是尽量避免使用。


# 犹豫的时候，就选用小 App 的方案

App 功能的拆分和设计是一门艺术，不是技术。所以以后可能需要拆分重组。

尽量使一个 App 足够小，多个小 App 相比一个大 App 更易维护。

# 一个 App 中有哪些模块？

## 常见的模块：

这些模块在 99% 的 Django App 中都能看到：

```
# Common modules
scoops/
    __init__.py
    admin.py
    forms.py
    management/
    migrations/
    models.py
    templatetags/
    tests/
    urls.py
    views.py
```

## 不太常见的模块

```
# uncommon modules
scoops/
    behaviors.py
    constants.py
    context_processors.py
    decorators.py
    db/
    exceptions
    fields.py
    factories.py
    helpers.py
    managers.py
    middleware.py
    signals.py
    utils.py
    viewmixins.py
```

各模块功能说明如下：

模块          | 功能说明
--------------|
constants.py  | App 级的设置值，如果 App 中设置值过多，应该独立出来放在该文件中
decorators.py | App 的装饰器
db/ 包        | 定制的数据模型项及其它数据库相关组件
fields.py     | 放置定制的数据模型项，如果数据库相关组件不多，可以只放在该文件中，无需创建 db 包
factories.py  | 产生测试数据的工厂函数
helpers.py    | 从 views.py 和 models.py 中提取出来的一些辅助功能函数
utils.py      | 同 helpers.py
managers.py   | 当 models.py 很大时，可以将定制的 model managers 抽取出来
signals.py    | 定制的信号
viewmixins.py | 从 views.py 中抽取出来的 mixins


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
