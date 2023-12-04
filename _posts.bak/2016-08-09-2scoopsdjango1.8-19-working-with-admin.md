---
title: 使用 Django Admin
date: 2016-08-09
writing-time: 2016-08-08 17:46--2016-08-09 10:42
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 它不是为终端用户准备的，它是为网站管理员准备的

# 使用 Admin 定制 vs 创建新的视图

相比于对 Django Admin 进行大量定制，通常创建一个相同功能的新视图会更简单。

# 对象的数据库表示

最佳实践：

+ 对每个 Django 数据模型都要实现其 **_str__** 方法，如果使用 python 2.7，使用 **django.utils.encoding.python_2_unicode_compatible** 装饰器。
+ 如果在数据模型的 admin 列表中还要显示其它的对象属性，使用 **list_display**。

实现 **__str__()__** 非常简单：

```python
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible # For Python 3.4 and 2.7
class IceCreamBar(models.Model):
    name = models.CharField(max_length=100)
    shell = models.CharField(max_length=100)
    filling = models.CharField(max_length=100)
    has_stick = models.BooleanField(default=True)

    def __str__(self):
        return self.name
```

对于 Python2.7，如果没有添加 **__str__()** 方法，Django 默认会提供一个 **__unicode__()** 方法。

而 **list_display** 的使用示例如下：

```python
from django.contrib import admin

from .models import IceCreamBar

class IceCreamBarAdmin(admin.ModelAdmin):
    list_display = ("name", "shell", "filling",)

admin.site.register(IceCreamBar, IceCreamBarAdmin)
```

# 在 ModelAdmin 类中添加可调用对象

为数据模型实例添加一个目标链接：

```python
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from icecreambars.models import IceCreamBar

class IceCreamBarAdmin(admin.ModelAdmin):

    list_display = ("name", "shell", "filling",)
    readonly_fields = ("show_url",)

    def show_url(self, instance):
        url = reverse("ice_cream_bar_detail",
                    kwargs={"pk": instance.pk})
        response = format_html("""<a href="{0}">{1}</a>""", url, url)
        return response

    show_url.short_description = "Ice Cream Bar URL"
    # Displays HTML tags
    # Never set allow_tags to True against user submitted data!!!
    show_url.allow_tags = True

admin.site.register(IceCreamBar, IceCreamBarAdmin)
```

由于 **allow_tags** 能将内容解析成 HTML 显示，存在安全隐患，故不要在用户提交的内容项上使用。

# 不在多用户环境下使用 list_editable

**django.contrib.admin** 中当使用 list_editable 时，普通 admin 列表视图会转成表单，使得管理员能同时编辑多条记录。但是，这些记录不是由其主键值标识的，而是通过其排列位置标识，因此，当有多个管理员同时进行编辑时，会出现错误。这是一个已知的 BUG。


# Django Admin 文档生成器

**django.contrib.admindocs** 包能检查项目中的各组件，如数据模型、视图、自定义模板 Tag 和自定义过滤器等，并自动生成文档。它对于查看项目的体系结构、对象名称等很有用。

安装步骤：

1. `pip install docutils` 到 virtualenv
2. 将 django.contrib.admindocs 添加到 INSTALLED_APPS
3. 将 `(r'^admin/doc/', include('django.contrib.admindocs.urls')` 添加到根 URLConf。确保添加到 `r'^admin/'` 项目前

之后，通过 `/admin/doc/` 即可访问。


# 加强 Django Admin 和 Django Admin Docs 的安全措施

# 使用自定义皮肤样式

相关皮肤包：

+ django-grappelli: 稳定、健壮
+ django-suit: 基于 Bootstrap，相对较新
+ django-admin-bootstrapped: 基于 Bootstrap

更多包，见 [admin-styling](https://www.djangopackages.com/grids/g/admin-styling/)

定制皮肤包是非常困难的，因此考虑评估使用第三方已实现的包。

## 评估点： 有没有好文档
## 如果自己定制，那么对每个定制的 Admin 扩展都要写测试


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
