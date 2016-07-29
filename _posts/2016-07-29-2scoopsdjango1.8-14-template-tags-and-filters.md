---
title: Django 模板的 Tag 和 Filter
date: 2016-07-29
writing-time: 2016-07-29 08:39--09:28
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

Django 默认模板 tag 和 filter 的特性：

+ 有清晰明白的命名
+ 只做一做事
+ 不会对任何持久化数据进行修改


# filter 本质就是函数

这种函数被限制只能接受一个或两个参数。一般来说，我们会在辅助函数模块中实现 filter 的功能函数，然后在定义 filter 的专门模块中导入相应的功能实现函数，从而最大限度地提高代码复用。

## filter 易于测试

因其只是函数，故易于测试。

## filter 与代码复用

如 Django 中的 *defaultfilter.py* ， 其大部分 filter 的逻辑都是从其它库导入的。例如， *django.template.defaultfilters.slugify* 只是 *django.utils.text.slugify* 的别名。在实现时，推荐将大部分逻辑都放在可重用的 *utils.py* 等模块中。

## 何时才写 filter

它只适用于修改数据的呈现方式。故在 REST API 输出或其它格式输出时适用。

# 自定义的模板 Tag

> Please stop writing so many template tags. They are a pain to debug.

## 模板 Tag 很难调试

## 模板 Tag 使代码难以复用

想复用，最好把代码放在 *utils.py* 等模块中。

## 模板 Tag 的性能欠佳

特别当 Tag 还需要导入大量的模板时，性能会更差。

## 何时才写 Tag

在写前，应考虑周全：

+ 有关读/写数据的操作最好应该放在数据模型等对象中
+ 项目的抽象基类能实现 Tag 的功能吗？


推荐自定义的模板 Tag 应该只实现 HTML 的呈现功能，比如呈现含有不同数据模型和数据类型的复杂的 HTML 布局等。

模板 Tag 相关的库：

+ django-crispy-forms
+ django-wysiwyg


# 模板 Tag 库的命名

应该为 **&lt;app_name&gt;_tags.py**，如 **flavors_tags**， **blog_tags.py**, **events_tags.py** 等。

库名千万不能和应用名相同，如 **flavors.py**， **blog.py** 等，鉴于 Django 导入模块 Tag 的方式，一定会出错。

# 加载模板 Tag 模块

应该用显式地方式加载，加载位置在 {% raw %}{% extends "base.html" %}{% endraw %} 之后，如下：

```jinja2
{% raw %}
{% extends "base.html" %}

{% load flavors_tags %}
{% endraw %}
```

## 不要隐式将 Tag 加载到内置区！！

不要这样做：

```
# Don't use this code!
# It's an evil anti-pattern!
from django import template
template.add_to_builtins(
    "flavors.templatetags.flavors_tags"
)
```

这种方式虽然遵循 DRY，但是它具有的缺点会把 DRY 的好处抵消殆尽：

+ 由于所有由 *django.template.Template* 加载的模板都会自动将 builtins 中的 Tag 加载进来，因此所有的继承子模板、模板中 {% raw %}{% include %} 语句、inclusion_tag 等都会重复加载这些 Tag 库，从而会影响性能
+ 由于是隐式加载，故难以调试

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
