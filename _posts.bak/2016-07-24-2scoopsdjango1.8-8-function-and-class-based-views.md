---
title: Django 基于函数和基于类的视图
date: 2016-07-24
writing-time: 2016-07-24 15:20--16:52
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

基于函数的视图 FBV 和 基于类的视图 CBV 都是有用的，没有哪种方式更好或已过时的说法。

# 何时使用 FBV 或 CBV

我们偏好使用 CBV，FBV 只使用在定制错误视图或那些使用 CBV 实现时会很复杂的情况。

# 视图逻辑不要放在 URLConf 中

路由信息保存在 *urls.py* 中。Django 的 URL 设计哲学是保持视图与 URL 的低耦合、无限灵活性和鼓励最佳实践。

URL 路由设计基本原则：

+ 视图模块应该只包含视图逻辑
+ URL 模块应该只包含 URL 逻辑


下面的代码就违背了 Django 的设计哲学：

```
from django.conf.urls import url
from django.views.generic import DetailView

from tastings.models import Tasting

urlpatterns = [
    url(r"ˆ(?P<pk>\d+)/$",
        DetailView.as_view(
            model=Tasting,
            template_name="tastings/detail.html"),
        name="detail"),
    url(r"ˆ(?P<pk>\d+)/results/$",
        DetailView.as_view(
            model=Tasting,
            template_name="tastings/results.html"),
        name="results"),
]
```

上面的代码中：

+ 视图和 URL 间高度耦合，使视图无法重用
+ 违背 DRY，相同/类似的参数使用了多次
+ URL 的无限灵活性被破坏，这里无法使用 CBV 的类继承的好处
+ 许多其它问题。如何添加认证功能？如何授权？如果在 URLConf 的每个视图上添加装饰器，会使该模块更加混乱


# 坚持 URLConf 中的低耦合

先定义视图：

```
# tastings/views.py
from django.views.generic import ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse

from .models import Tasting

class TasteListView(ListView):
    model = Tasting

class TasteDetailView(DetailView):
    model = Tasting

class TasteResultsView(TasteDetailView):
    template_name = "tastings/results.html"

class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse("tastings:detail",
            kwargs={"pk": self.object.pk})
```

再定义 URL：

```
# tastings/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r"ˆ$",
        view=views.TasteListView.as_view(),
        name="list"
    ),
    url(
        regex=r"ˆ(?P<pk>\d+)/$",
        view=views.TasteDetailView.as_view(),
        name="detail"
    ),
    url(
        regex=r"ˆ(?P<pk>\d+)/results/$",
        view=views.TasteResultsView.as_view(),
        name="results"
    ),
    url(
        regex=r"ˆ(?P<pk>\d+)/update/$",
        view=views.TasteUpdateView.as_view(),
        name="update"
    )
]
```

优点是：

+ DRY：各视图间没有重复的参数或属性
+ 低耦合：将数据模型和模板名从 URLConf 中移除，因为视图应该只含视图逻辑，而 URLConf 应该只含 URL 逻辑。这样我们就能在多个 URLConf 中调用我们的视图了
+ URLConf 应该只做一件事并且做好它：现在的 URLConf 只专注 URL 路由
+ 我们的视图能利用 CBV 的优点：视图可以继承，可以加装饰器
+ 无限灵活性：由于视图被正式定义，可以实现任意逻辑

# 使用 URL 命名空间

它能为应用级和实例级命名空间提供一个标识。

URL 名不要写成这样 **tastings_details**，而应该这样 **tastings:detail**。

URLConf 的例子如下：

```
# urls.py at root of project
urlpatterns += [
    url(r'ˆtastings/', include('tastings.urls', namespace='tastings')),
]
```

在 视图中的例子如下：

```
# tastings/views.py snippet
class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse("tastings:detail",
            kwargs={"pk": self.object.pk})
```

在模板中的例子：

```jinja2
{% raw %}
{% extends "base.html" %}

{% block title %}Tastings{% endblock title %}

{% block content %}
<ul>
  {% for taste in tastings %}
    <li>
      <a href="{% url "tastings:detail" taste.pk %}">{{ taste.title }}</a>
      <small>
        (<a href="{% url "tastings:update" taste.pk %}">update</a>)
      </small>
    </li>
  {% endfor %}
</ul>
{% endblock content %}
{% endraw %}
```

## 命名空间使 URL 名更短、更明显及 DRY

相比于用 **tastings_detail**，使用 **detail** 使应用的代码更清晰。

## 提高了与第三方库的交互性

可以解决应用的名字冲突。比如已经有了一个 contact 应用，现在还想再增加一个 contact 应用，可以：

```
# urls.py at root of project
urlpatterns += [
    url(r'ˆcontact/', include('contactmonger.urls',
                            namespace='contactmonger')),
    url(r'ˆreport-problem/', include('contactapp.urls',
                            namespace='contactapp')),
]
```

然后在模板中：

```jinja2
{% raw %}
{% extends "base.html" %}
{% block title %}Contact{% endblock title %}
{% block content %}
<p>
  <a href="{% url "contactmonger:create" %}">Contact Us</a>
</p>
<p>
  <a href="{% url "contactapp:report" %}">Report a Problem</a>
</p>
{% endblock content %}
{% endraw %}
```

## 更易查找、升级和重构

查找像 **tastings_detail** 这样的代码或名字较难，而 **tastings:detail** 更明显。

# 在 URLConf 中对视图的引用不要用字符串

Django 1.8 之前的 url.py 是这样的：

```
# DON'T DO THIS!
# polls/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Defining the view as a string
    url(r'ˆ$', 'polls.views.index', name='index'),
)
```

这种方式有几下问题：

+ Django 会隐式加载视图函数/类。当视图出错时，这种隐式加载方式使调试更难
+ 需要对初学者讲解 urlpatterns 开头的空字符串的作用


以下是推荐的写法：

```
# polls/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    # Defining the views explicitly
    url(r'ˆ$', views.index, name='index'),
]
```


# 不要将业务逻辑放在视图中

将业务逻辑放在视图中会使视图代码量越来越大，难以维护。将业务逻辑放在数据模型的方法、管理器的方法或者工具辅助函数模块中。

# Django 视图都是函数

Django 视图本质上都是函数，它接受一个 HTTP 请求对象，然后返回一个 HTTP 应答对象。类比于数学中的函数：

```
# Django FBV as a function
HttpResponse = view(HttpRequest)

# Deciphered into basic math (remember . functions from algebra?)
y = f(x)

# ... and then translated into a CBV example
HttpResponse = View.as_view()(HttpRequest)
```

## 最简单的视图

```
# simplest_views.py
from django.http import HttpResponse
from django.views.generic import View

# The simplest FBV
def simplest_view(request):
    # Business logic goes here
    return HttpResponse("FBV")

# The simplest CBV
class SimplestView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here
        return HttpResponse("CBV")
```

# 不能用 locals() 的返回作为视图的 Context

不能这样写：

```
def ice_cream_store_display(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    date = timezone.now()
    return render(request, 'melted_ice_cream_report.html', locals())
```

表面上看起来好像没有问题，但是一旦视图进行了重构，将局部变量名改名，有可能会影响模板的使用，如：

```
def ice_cream_store_display(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    now = timezone.now()
    return render(request, 'melted_ice_cream_report.html', locals())
```

此时，将 date 改成 now 可以会有影响。

故强烈建议在视图上下文对象中显式定义，如：

```
def ice_cream_store_display(request, store_id):
    return render(request, 'melted_ice_cream_report.html', dict{
        'store': get_object_or_404(Store, id=store_id),
        'now': timezone.now()
    })
```

相关资源: [Django template and the locals trick](http://stackoverflow.com/questions/1901525/django-template-and-the-locals-trick#1901720)


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
