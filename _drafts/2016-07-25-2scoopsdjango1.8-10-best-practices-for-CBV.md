---
title: CBV 最佳实践
date: 2016-07-25
writing-time: 2016-07-25 10:00
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

Django 视图本质是一个函数：接受 HttpRequest 对象作为参数，返回一个 HttpResponse 对象作为返回。FBV 直接就是这样一个函数，而 CBV 类的方法 as_view()，它的返回也是这样一个函数。

Django 同时提供了一些通用视图， generic class-based views (GCBV)，可以加快开发。

**django.views.generic** 中提供的这些 GCBV，或者 mixin 还不够完善，没有包括认证等功能。因此，可采用 **django-braces** 这个第三方库来弥补空白。


# CBV 代码编写指南：

+ 视图代码越少越好
+ 视图代码不能重复
+ 视图应该只处理呈现逻辑。业务逻辑应放在数据模型中，或者表单对象中
+ 保持视图代码简单
+ 不要用 CBV 来实现自定义的 403, 404 和 500 等错误处理器，应使用 FBV
+ 保持 mixins 简洁


# 在 CBV 中使用 Mixins

子类通过多重继承 Mixin，可以将 Mixin 中的功能和行为包含进自身来。

因此，我们可以利用 Mixin 的功能来组装我们的视图类。

使用 Mixin 时，推荐遵循 kenneth Love 的继承规则，该规则也是从左到右进行处理的，和 Python 的方法解决规划类似：

+ Django 提供的基类移到右边
+ Mixin 放在左边
+ Mixin 应该继承自 object

一个简单的例子如下：

```
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

下表列出了 django.views.generic 下的各 GCBV 的用途：

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

+ 尽量利用 Django 提供的所有通用视图。推荐信奉这种观点
+ 只使用　django.views.generic.View
+ 尽量避免使用 CBV，先都有 FBV，只在必要时改用 CBV


# 关于 Django CBV 的通用建议

## 如果限制 CBV/GCBV 只能由认证用户访问

**django.contrib.auth.decorators.login_required** 装饰器应用到 CBV 比较 麻烦，应使用 django-braces 提供的 **LoginRequiredMixin**，例如：

```
# flavors/views.py
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorDetailView(LoginRequiredMixin, DetailView):
    model = Flavor
```

## 表单有效时在视图的 form_valid() 中进行后续处理

在调用 form_valid() 时，表单内的所有数据总已验证过，并且都有效。
form_valid() 应该返回一个 django.http.HttpResponseRedirect 对象。

例如：

```
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

```
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

可以在模板代码中，通过 view 对象本身，调用相关的属性和方法。

例如，定义的视图如下：

```
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

{% highlight %}
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
{% endhighlight %}


# GCBV 和表单如何结合使用

































> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
