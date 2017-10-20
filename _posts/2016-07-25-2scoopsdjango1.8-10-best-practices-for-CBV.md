---
title: Django 的 CBV 最佳实践
date: 2016-07-25
writing-time: 2016-07-25 10:00--16:15
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

Django 视图本质是一个函数：接受 HttpRequest 对象作为参数，返回一个 HttpResponse 对象作为返回。FBV 直接就是这样一个函数，而 CBV 类的方法 as_view()，它的返回也是这样一个函数。

Django 提供了一些通用视图， generic class-based views (GCBV)，可以加快开发。

**django.views.generic** 中提供的这些 GCBV，或者 Mixin 还不够完善，没有包括认证等功能。因此，可采用 **django-braces** 这个第三方库来弥补空缺。


# CBV 代码编写指南：

+ 视图代码越少越好
+ 视图代码不能重复
+ 视图应该只处理呈现逻辑。业务逻辑应放在数据模型中，或者表单对象中
+ 保持视图代码简单
+ 不要用 CBV 来实现自定义的 403, 404 和 500 等错误处理器，应使用 FBV 实现
+ 保持 Mixins 简洁


# 在 CBV 中使用 Mixins

子类通过多重继承 Mixin，可以将 Mixin 中的功能和行为包含进自身。

因此，我们可以利用 Mixin 的功能来组装我们的视图类。

使用 Mixin 时，推荐遵循 kenneth Love 的继承规则，该规则也是从左到右进行处理的，和 Python 的方法解析规则类似：

+ Django 提供的基类移到右边
+ Mixin 放在左边
+ Mixin 应该继承自 object

一个简单的例子如下：

```python
from django.views.generic import TemplateView

class FreshFruitMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FreshFruitMixin,
                        self).get_context_data(**kwargs)
        context["has_fresh_fruit"] = True
        return context

class FruityFlavorView(FreshFruitMixin, TemplateView):
    template_name = "fruity_flavor.html"
```

# 哪个 Django GCBV 应该用于哪个任务？

GCBV 的可重用性是以牺牲易用性为代价的。GCBV 有复杂的继承关系链。

下表列出了 django.views.generic 中的各 GCBV 的用途：

名称         | 目的                   | 例子
-------------|------------------------|
View         | 视图基础类             | 使用 django.views.generic.View
RedirectView | 重定向到 URL           | 如重定向到 '/login/'
TemplateView | 显示 HTML 模板         | 如 '/about/' 页
ListView     | 列出对象               |
DetailView   | 对象的详细信息         |
FormView     | 提交表单               |
CreateView   | 创建对象               |
UpdateView   | 更新对象               |
DeleteView   | 删除对象               |
通用时间视图 | 显示某个时间段内的对象 |


## 如何利用 Django CBV/GCBV 的三种观点：

+ 尽量利用 Django 提供的所有通用视图。推荐这种观点
+ 只使用　django.views.generic.View
+ 尽量避免使用 CBV，先都有 FBV，只在必要时改用 CBV


# 关于 Django CBV 的通用建议

## 如何限制 CBV/GCBV 只能由认证用户访问

**django.contrib.auth.decorators.login_required** 装饰器应用到 CBV 比较麻烦，应使用 django-braces 提供的 **LoginRequiredMixin**，例如：

```python
# flavors/views.py
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorDetailView(LoginRequiredMixin, DetailView):
    model = Flavor
```

## 表单有效时在视图的 form_valid() 中进行后续处理

在调用 form_valid() 时，表单内的所有数据都已验证过，并且都有效。
form_valid() 应该返回一个 django.http.HttpResponseRedirect 对象。

例如：

```python
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

    def form_valid(self, form):
        # Do custom logic here
        return super(FlavorCreateView, self).form_valid(form)
```

## 表单无效时在视图的 form_invalid() 中进行后续处理

如果表单的数据在验证时无效，会调用该方法，该方法应该返回一个 django.http.HttpResponse 对象。

例如：

```python
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor

    def form_invalid(self, form):
        # Do custom logic here
        return super(FlavorCreateView, self).form_invalid(form)
```

## 在模板中引用视图 view 对象

可以在模板代码中，通过 view 对象变量，调用相关的属性和方法。

例如，定义的视图如下：

```python
from django.utils.functional import cached_property
from django.views.generic import UpdateView, TemplateView

from braces.views import LoginRequiredMixin

from .models import Flavor
from .tasks import update_users_who_favorited

class FavoriteMixin(object):

    @cached_property
    def likes_and_favorites(self):
        """Returns a dictionary of likes and favorites"""
        likes = self.object.likes()
        favorites = self.object.favorites()
        return {
            "likes": likes,
            "favorites": favorites,
            "favorites_count": favorites.count(),
        }

class FlavorUpdateView(LoginRequiredMixin, FavoriteMixin, UpdateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

    def form_valid(self, form):
        update_users_who_favorited(
            instance=self.object,
            favorites=self.likes_and_favorites['favorites']
        )
        return super(FlavorCreateView, self).form_valid(form)

class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, TemplateView):
    model = Flavor
```

然后在模板代码中，访问视图对象：

```jinja2
{% raw %}
{# flavors/base.html #}
{% extends "base.html" %}

{% block likes_and_favorites %}
<ul>
  <li>Likes: {{ view.likes_and_favorites.likes }}</li>
  <li>Favorites: {{ view.likes_and_favorites.favorites_count }}</li>
</ul>
{% endblock likes_and_favorites %}
{% endraw %}
```

# GCBV 和表单如何结合使用

以下例子中使用的数据模型定义如下：

```python
# flavors/models.py
from django.core.urlresolvers import reverse
from django.db import models

STATUS = (
    (0, "zero"),
    (1, "one"),
)

class Flavor(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    scoops_remaining = models.IntegerField(default=0, choices=STATUS)

    def get_absolute_url(self):
        return reverse("flavors:detail", kwargs={"slug": self.slug})
```

下面是使用表单的几种场景：

## 1、Views + ModelForm

这是最简单最常见的表单场景。当创建数据模型后，通常需要能够添加一条新记录、更新记录。

以下例子将创建一些视图来对 Flavor 记录进行创建、更新和显示。同时演示如何向用户提供消息提醒。

+ FlavorCreateView 对应创建新记录的表单
+ FlavorUpdateView 对应更新记录的表单
+ FlavorDetailView 显示记录详情，并作为创建和更新操作的确认页显示

视图代码如下：

```python
# flavors/views.py
from django.views.generic import CreateView, UpdateView, DetailView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

class FlavorUpdateView(LoginRequiredMixin, UpdateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

class FlavorDetailView(DetailView):
    model = Flavor
```

由于 FlavorDetailView 要作为操作确认界面，需要对不同的操作提醒不同的消息。可以使用 **django.contrib.messages** 的相关功能完成。

下面将重载 FlavorCreateView 和 FlavorUpdateView 的 form_valid() 方法，实现当操作完成后推送不同的消息。可以将重复的代码提取出来，放在一个 Mixin 中，如下：

```python
# flavors/views.py

from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorActionMixin(object):

    fields = ('title', 'slug', 'scoops_remaining')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,
                        CreateView):
    model = Flavor
    success_msg = "Flavor created!"

class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,
                        UpdateView):
    model = Flavor
    success_msg = "Flavor updated!"

class FlavorDetailView(DetailView):
    model = Flavor
```

当 FlavorCreateView 或 FlavorUpdateView 操作完成后，FlavorDetailView 的模板代码就可以通过访问 messages 变量来获取相关推送消息了，如下：

```jinja2
{% raw %}
{# templates/flavors/flavor_detail.html #}
{% if messages %}
  <ul class="messages">
    {% for message in messages %}
    <li id="message_{{ forloop.counter }}"
      {% if message.tags %} class="{{ message.tags }}"
        {% endif %}>
      {{ message }}
    </li>
    {% endfor %}
  </ul>
{% endif %}
{% endraw %}
```

以上的模板代码可以放在项目的 BASE 模板中。

## 2、Views + Form

以查询表单为例，先显示一个查询表单页，提交后通过 ORM 查询，将查询结果列表显示出来。

在本例中，只实现一个 FlavorListView，将查询表单和查询结果全部都显示在该页中。

由于查询没有修改数据，因此表单方法用 **GET**。要正确显示匹配的查询列表，需要重载 ListView 的 get_queryset() 方法，视图代码如下：

```python
from django.views.generic import ListView

from .models import Flavor

class FlavorListView(ListView):
    model = Flavor

    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset
        queryset = super(FlavorListView, self).get_queryset()

        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # Return a filtered queryset
            return queryset.filter(title__icontains=q)
        # Return the base queryset
        return queryset
```

由于查询框表单可能会出现在多个页面中，因此将这部分代码片段保存在 *_flavor_search.html*，方便在其它模板文件中导入，代码如下：


```jinja2
{% raw %}
{# templates/flavors/_flavor_search.html #}
{% comment %}
    Usage: {% include "flavors/_flavor_search.html" %}
{% endcomment %}
<form action="{% url "flavor_list" %}"  method="GET">
    <input type="text" name="q" />
    <button type="submit">search</button>
</form>
{% endraw %}
```

# 只使用 django.views.generic.View

FBV 如果要区别不同的 HTTP 方法，需要用 if 块，而 CBV 只需定义 get()，post() 方法即可，比较清晰明了。

如下面的代码所示，继承 View 类后，CBV 只需定义 get()，post() 就能完成相应的 HTTP 请求。

```python
from braces.views import LoginRequiredMixin

from .forms import FlavorForm
from .models import Flavor

class FlavorView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Handles display of the Flavor object
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
        return render(request,
            "flavors/flavor_detail.html",
                {"flavor": flavor}
            )

    def post(self, request, *args, **kwargs):
        # Handles updates of the Flavor object
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
        form = FlavorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("flavors:detail", flavor.slug)
```

这种写法和 FBV 类似，但是更加清晰，而且也可以加入 Mixin。

它最适合用来输出 JSON、PDF、Excel 等非 HTML 内容。如下例如下：

```python
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from braces.views import LoginRequiredMixin

from .models import Flavor
from .reports import make_flavor_pdf

class PDFFlavorView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Get the flavor
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])

        # create the response
        response = HttpResponse(content_type='application/pdf')

        # generate the PDF stream and attach to the response
        response = make_flavor_pdf(response, flavor)

        return response
```

实际上，这种方式即保持了 FBV 的简单，又具有了 CBV 的继承优势。


# 其它资源

+ http://2scoops.co/1.8-topics-class-based-views
+ http://2scoops.co/1.8-cbv-generic-display
+ http://2scoops.co/1.8-cbv-generic-editing
+ http://2scoops.co/1.8-cbv-mixins
+ http://2scoops.co/1.8-ref-class-based-views
+ [GCBV inspector](http://ccbv.co.uk)
+ http://www.python.org/download/releases/2.3/mro/
+ http://pydanny.com/tag/class-based-views.html


其它包：

+ django-extra-views: 包含了一些 django-braces 没有提供的功能
+ django-vanilla-views: 将 Django GCBV 的功能以更简单、易用的方式提供，可和 Django-braces 一起使用。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
