---
title: Django 的 FBV 最佳实践
date: 2016-07-25
writing-time: 2016-07-25 09:04--09:57
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# FBV 的优势

FBV 简单易懂，但是难以复用。它们不能像 CBV 那样能从父类中继承。

FBV 的编写指南：

+ 视图代码越少越好
+ 视图代码不能重复
+ 视图应该只处理呈现逻辑。业务逻辑应尽可能放在数据模型中，或者表单对象中
+ 视图代码要保持简单
+ 使用它们来编写自定义的 403, 404, 500 等错误处理器
+ 避免使用嵌套的 if 块


# 传递 HttpRequest 对象

辅助函数应将 django.http.HttpRequest 对象作为主要参数，然后从该参数中获取属性和方法。

比如：

```
# sprinkles/utils.py

from django.core.exceptions import PermissionDenied

def check_sprinkle_rights(request):
    if request.user.can_sprinkle or request.user.is_staff:
        return request

    # Return a HTTP 403 back to the user
    raise PermissionDenied
```

辅助函数可以返回 HttpRequest 对象，并且可以在返回的对象中增加额外的属性，比如：

```
# sprinkles/utils.py

from django.core.exceptions import PermissionDenied

def check_sprinkles(request):
    if request.user.can_sprinkle or request.user.is_staff:
        # By adding this value here it means our display templates
        # can be more generic. We don't need to have
        # {% raw %}{% if request.user.can_sprinkle or request.user.is_staff %}{% endraw %}
        # instead just using
        # {% raw %}{% if request.can_sprinkle %}{% endraw %}
        request.can_sprinkle = True
        return request

    # Return a HTTP 403 back to the user
    raise PermissionDenied
```

之后，可以对新增的属性加以利用，如：

```
# sprinkles/views.py

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .utils import check_sprinkles
from .models import Sprinkle

def sprinkle_list(request):
    """Standard list view"""

    request = check_sprinkles(request)

    return render(request,
        "sprinkles/sprinkle_list.html",
        {"sprinkles": Sprinkle.objects.all()})

def sprinkle_detail(request, pk):
    """Standard detail view"""
    request = check_sprinkles(request)

    sprinkle = get_object_or_404(Sprinkle, pk=pk)

    return render(request, "sprinkles/sprinkle_detail.html",
        {"sprinkle": sprinkle})

def sprinkle_preview(request):
    """"preview of new sprinkle, but without the
        check_sprinkles function being used.
    """
    sprinkle = Sprinkle.objects.all()
    return render(request,
        "sprinkles/sprinkle_preview.html",
        {"sprinkle": sprinkle})
```

# 尽量使用装饰器


“语法糖” 就是新增到编程语言中的某种语法，它使代码更加易读，或者表达能力更强。而 Python 中的装饰器就是这样的一种语法糖。

装饰器也使代码能被重用。

下面是装饰器的代码模板，这种装饰器可用于 FBV：

```
# simple decorator template
import functools

def decorator(view_func):
    @functools.wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        # You can modify the request (HttpRequest) object here.
        response = view_func(request, *args, **kwargs)
        # You can modify the response (HttpResponse) object here.
        return response
    return new_view_func
```

上面模板中的 **functools.wraps()**，用来将原函数的 docstrings 等元数据复制到装饰后的新函数中，它可使代码更易维护。

根据上面的模板，实现以下的装饰器：

```
# sprinkles/decorators.py
from functools import wraps

from . import utils

# based off the decorator template
def check_sprinkles(view_func):
    """Check if a user can add sprinkles"""
    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        # Act on the request object with utils.can_sprinkle()
        request = utils.can_sprinkle(request)

        # Call the view function
        response = view_func(request, *args, **kwargs)

        # Return the HttpResponse object
        return response
    return new_view_func
```

然后运用该装饰器：

```
# views.py
from django.shortcuts import get_object_or_404, render

from .decorators import check_sprinkles
from .models import Sprinkle

# Attach the decorator to the view
@check_sprinkles
def sprinkle_detail(request, pk):
    """Standard detail view"""

    sprinkle = get_object_or_404(Sprinkle, pk=pk)

    return render(request, "sprinkles/sprinkle_detail.html",
        {"sprinkle": sprinkle})
```

## 装饰器的采用要保守

装饰器是个强大的工具，用多了会使代码看起来很复杂。因此，应该限制在一个视图上最多能加几个装饰器，并坚持这个原则。

相关资源：

+ [Improve Your Python: Decorators Explained](http://jeffknupp.com/blog/2013/11/29/improve-your-python-decorators-explained/)
+ [Decorators and Functional Python](http://www.brianholdefehr.com/decorators-and-functional-python)
+ [Python Decorator Cheatsheet](http://www.pydanny.com/python-decorator-cheatsheet.html)

# 传递 HttpResponse 对象

这和在辅助函数中传递 HttpRequest 对象的情况是类似的。也可 Middleware.process_request() 方法类似。当然，也可以用装饰器实现。

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
