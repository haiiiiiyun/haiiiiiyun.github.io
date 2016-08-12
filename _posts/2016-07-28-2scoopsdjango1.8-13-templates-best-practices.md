---
title: Django 模板最佳实践
date: 2016-07-28
writing-time: 2016-07-28 14:29--16:53
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

Django 大大限制了模板语言的功能，从而迫使我们将业务逻辑使用 Python 代码实现。

# 将模板文件保存在主 templates/ 下

推荐将模板文件保存在项目的 templates/ 目录下，并根据子应用建立相应的子目录，如：

```
templates/
    base.html
    ... (other sitewide templates in here)
    freezers/
        ("freezers" app templates in here)
```

过去推荐将子应用的模板文件放在其自身的 templates 目录下，如：

```
freezers/
    templates/
        freezers/
            ... ("freezers" app templates in here)
templates/
    base.html
    ... (other sitewide templates in here)
```

这种方式嵌套太多。

要对安装的第三方应用的模板进行覆盖，应将覆盖的模板文件放置在项目主 templates/ 目录下的相应位置。


# 模板体系结构模式

简单的 2 层 和 3 层是较理想的体系结构。

## 2 层模板体系结构的例子

```
templates/
    base.html
    dashboard.html # extends base.html
    profiles/
        profile_detail.html # extends base.html
        profile_form.html # extends base.html
```

所有的模板都扩展至一个基模板文件。

## 3 层模板体系结构的例子

```
templates/
    base.html
    dashboard.html # extends base.html
    profiles/
        base_profiles.html # extends base.html
        profile_detail.html # extends base_profiles.html
        profile_form.html # extends base_profiles.html
```

+ 每个子应用都有各自的基模板 *base_&lt;app_name&gt;.html*，并有共同的父基模板 *base.html*。
+ 子应用中的所有模板共用相同的父模板 *base_&lt;app_name&gt;.html*。
+ 和 *base.html* 同级的模板都继承自 *base.html*。


## 扁平优于嵌套

# 限制模板中的处理工作

应尽量减少模板中的处理工作。特别当在模板中进行查询和遍历时，应考虑周全。

假设我们有一个免费申请试用的应用，其数据模型定义如下：

```python
# vouchers/models.py
from django.core.urlresolvers import reverse
from django.db import models
from .managers import VoucherManager

class Voucher(models.Model):
    """Vouchers for free pints of ice cream."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    birth_date = models.DateField(blank=True)
    sent = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)

    objects = VoucherManager()
```

下面根据该数据模型演示几种需要避免的情况。

## 情况1： 避免在模板中做数据聚合操作

将聚合等逻辑操作放在 Python 代码中，模板只进行显示操作。

例如，要将申请人的人数按年龄段分开统计，不要将聚合和统计操作放在模板中实现，在该例中，可以放在数据模型的 Manager 中实现：

```python
# vouchers/managers.py
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from django.db import models

class VoucherManager(models.Manager):
    def age_breakdown(self):
        """Returns a dict of age brackets/counts."""
        age_brackets = []
        now = timezone.now()

        delta = now - relativedelta(years=18)
        count = self.model.objects.filter(birth_date__gt=delta).count()
        age_brackets.append(
            {"title": "0-17", "count": count}
        )

        count = self.model.objects.filter(birth_date__lte=delta).count(
        age_brackets.append(
            {"title": "18+", "count": count}
        )
        return age_brackets
```

然后在模板中只进行数值的显示操作：

```jinja2
{% raw %}
# templates/vouchers/ages.html #}
{% extends "base.html" %}

{% block content %}
<table>
    <thead>
        <tr>
            <th>Age Bracket</th>
            <th>Number of Vouchers Issued</th>
        </tr>
    </thead>
    <tbody>
        {% for age_bracket in age_brackets %}
        <tr>
            <td>{{ age_bracket.title }}</td>
            <td>{{ age_bracket.count }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock content %}
{% endraw %}
```

## 情况 2：避免在模板中进行条件过滤

假如想过滤名字为 Greenfelds 和 Roys 的申请人，不要在模板中进行过滤，如下所示：

```jinja2
{% raw %}
<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
{% for voucher in voucher_list %}
    {# Don't do this: conditional filtering in templates #}
        {% if "greenfeld" in voucher.name.lower %}
        <li>{{ voucher.name }}</li>
    {% endif %}
{% endfor %}
</ul>

<h2>Roys Who Want Ice Cream</h2>
<ul>
{% for voucher in voucher_list %}
    {# Don't do this: conditional filtering in templates #}
    {% if "roy" in voucher.name.lower %}
        <li>{{ voucher.name }}</li>
    {% endif %}
{% endfor %}
</ul>
```

应该将条件过滤操作用 ORM 实现，并将结果放在模板上下文变量中：

```python
# vouchers/views.py
from django.views.generic import TemplateView

from .models import Voucher

class GreenfeldRoyView(TemplateView):
    template_name = "vouchers/views_conditional.html"

    def get_context_data(self, **kwargs):
        context = super(GreenfeldRoyView, self).get_context_data(**kwargs)
        context["greenfelds"] = \
            Voucher.objects.filter(name__icontains="greenfeld")
        context["roys"] = Voucher.objects.filter(name__icontains="roy")
    return context
```

然后在模板中进行简单的显示操作：

```jinja2
{% raw %}
<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
{% for voucher in greenfelds %}
    <li>{{ voucher.name }}</li>
{% endfor %}
</ul>

<h2>Roys Who Want Ice Cream</h2>
<ul>
{% for voucher in roys %}
    <li>{{ voucher.name }}</li>
{% endfor %}
</ul>
{% endraw %}
```

## 情况 3：避免在模板中使用隐含有复杂查询的操作

例如下面的代码，会触发很多的隐含查询操作：

```jinja2
{% raw %}
{# list generated via User.object.all() #}
<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
{% for user in user_list %}
    <li>
        {{ user.name }}:
        {# DON'T DO THIS: Generated implicit query per user #}
        {{ user.flavor.title }}
        {# DON'T DO THIS: Second implicit query per user!!! #}
        {{ user.flavor.scoops_remaining }}
    </li>
{% endfor %}
</ul>
{% endraw %}
```

要减少隐含查询操作，可以使用 Django ORM 的 **select_related()** 方法：


## 情况 4： 避免在模板中调用 CPU 高负载的操作

像图像处理（sorl-thumbnail）等操作，通常还需要将数据保存到文件系统中，往往需要大量的处理时间，从而影响网站性能。因此应将这些操作移到视图、数据模型、辅助函数、或者异步消息队列（如 Celery）中操作。

## 情况 5：避免在模板中使用含 REST API 调用的操作

在模板中调用第三方服务（如地图 API）通常会影响性能。

应该：

+ 将加载操作移到客户端的 Javascript 代码中实现
+ 将会拖慢视图处理速度的代码用其它方式实现，如消息队列，线程或多处理器等

# 不要在意产生的 HTML 源文件是否好看

要在意的是模板源文件的可维护性。

# 应该牢记的几条有用建议

## 避免将风格信息与 Python 代码关联

风格信息应该放在 CSS 文件中。

## 常用约定

+ 模板名、块名等模板中的名称应使用下划线 `_`，不要用破折号 `-`。
+ 块名应该清楚直白。如 {% raw %}{% block javascript %}{% endraw %}
+ 块结束答要加上块名，如 {%raw %}{% endblock javascript %}{% endraw %}
+ 需被其它模板导入的模板文件名，用 `_` 开头。

## 模板文件位置

模板文件应该放在项目根目录的 templates 下。除非你想打包成一个 Django 包进行发布。

## 使用命名的上下文对象

当使用通用 CBV 时，在模板中即可以用 `object_list` 和 `object` 这样的通用名称，也可以用基于数据模型（如 Topping）的名称，如 `topping_list` 和 `topping` 这样的命名对象。推荐使用后者。

## 模板中使用命名的 URL，不要硬编码路径和 URL

## 调试复杂的模板

可以设置 `string_if_invalid`，输出更加详细的模板调试内容：

```python
# settings/local.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'string_if_invalid': 'INVALID EXPRESSION: %s'
         }
    },
]
```

# 错误页模板

至少为 404 和 500 错误创建模板文件，如 404.html 和 500.html。

错误页应该部署在独立的静态文件服务器上，如 Nginx 和 Apache，这样，当你的 Django 网站挂掉时，错误页还能看到。

如果使用 Heroku 等 PaaS，要参阅其相应的文档。

参照 Github 的 [404](https://github.com/404) 和 [500](https://github.com/500) 页，得出错误页应该：

+ 所有的 CSS 内容应该包含在该相同的 HTML 文件中。
+ 所有的图片都以 data 的方式保存在相同的 HTML 文件中，不要用 img 或外部 URL
+ 所有的 Javascript 也应包含在该相同的 HTML 文件中。

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
