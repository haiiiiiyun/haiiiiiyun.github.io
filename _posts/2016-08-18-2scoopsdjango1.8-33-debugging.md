---
title: 持续集成
date: 2016-08-18
writing-time: 2016-08-18 13:49--14:40
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 开发环境下的调试

## 使用 django-debug-toolbar

它能显示有关当前请求/应答周期中的各种调试信息，如模板呈现时间、查询操作、哪些变量等

+ https://pypi.python.org/pypi/django-debug-toolbar
+ http://django-debug-toolbar.readthedocs.org


## 去除这个讨厌的 CBV 错误

直接将 CBV 的类作为 url 的参数，不加 as_view()，会出现如下错误提示：

```conf
twoscoopspress$ python discounts/manage.py runserver 8001
Starting development server at http://127.0.0.1:8001/
Quit the server with CONTROL-C.
Internal Server Error: /
Traceback (most recent call last):
File "/Users/python/lib/python2.7/site-packages/django/core/handlers/base.py",
line 132, in get_response response = wrapped_callback(request,
*callback_args, **callback_kwargs)
File "/Users/python/lib/python2.7/site-packages/django/utils/decorators.py",
line 145, in inner
return func(*args, **kwargs)
TypeError: __init__() takes exactly 1 argument (2 given)
```

## 掌握 Python 调试器

PDB 用于：

1. 测试中
2. 调试管理命令中

注意：在生产环境中不要有 Pdb 断点，它会中止代码执行。

当 PDB 由 ipdb 扩展后，功能会更加强大。

相关资料：

+ [Python’s pdb documentation](https://docs.python.org/2/library/pdb.html)
+ [IPDB](https://pypi.python.org/pypi/ipdb)
+ [Using PDB with Django](https://mike.tig.as/blog/2010/09/14/pdb/)

## 记住表单文件上传的本质

1. &lt;form&gt; 标签是否已包含了编码类型 enctype ？

```jinja
{% raw %}
<form action="{% url 'stores:file_upload' store.pk %}"
            method="post"
            enctype="multipart/form-data">
{% endraw %}
```

2. 视图是否对 **request.FILES** 进行了处理？

FBV:

```python
# stores/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from stores.forms import UploadFileForm
from stores.models import Store

def upload_file(request, pk):
    """Simple FBV example"""
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        # Don't forget to add request.FILES!
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            store.handle_uploaded_file(request.FILES['file'])
            return redirect(store)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form, 'store': store})
```


CBV:

```python
# stores/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from stores.forms import UploadFileForm
from stores.models import Store

class UploadFile(View):
    """Simple CBV example"""
    def get_object(self):
        return get_object_or_404(Store, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        store = self.get_object()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            store.handle_uploaded_file(request.FILES['file'])
            return redirect(store)
        return redirect('stores:file_upload', pk=pk)

    def get(self, request, *args, **kwargs):
        store = self.get_object()
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form, 'store': store})
```

# 在生产环境下调试

有些 BUG 只在特定条件下会出现，如负载情况、第三方 API 及数据量等。

## 用更便捷的方式查看日志

日志量可能很多，因此最好通过类似 Sentry 等的日志聚集工具进行查看。

## 制作生产环境的镜像

步骤：

1. 在防火墙或其它保护措施下，配置一个与生产环境一样的远程主机
2. 复制数据，注意要去除与个人相关的数据。

设置好后，尝试重现 BUG，因为该服务器在防火墙后，故可以将 settings.DEBUG 设置为 True

## 使用基于用户的异常中间件

在生产环境中将 settings.DEBUG 设置为 True 会有安全问题。但是基于特定用户来显示调试信息将不会有安全问题：

```python
# core/middleware.py
import sys

from django.views.debug import technical_500_response

class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
```

## 非常烦人的 settings.ALLOWED_HOSTS 错误

ALLOWED_HOSTS 列出了 Django 站点能提供服务的主机/域名列表。当 settings.DEBUG 设置为 False 时，必须将该值设置起来。没有设置好该配置项的网站会一直产生 500 错误，而且日志中会有 SuspiciousOperation 错误。

正确配置的例子：

```python
# settings.py
ALLOWED_HOSTS = [
    '.djangopackages.com',
    'localhost', # Ensures we can run DEBUG = False locally
    '127.0.0.1' # Ensures we can run DEBUG = False locally
]
```

# 功能开关

当有新功能开发完成后，如果可以在 admin 界面中指定哪些用户可以使用这些新功能，将对新功能的测试及其 BUG 产生的影响很有帮助。

## 功能开关相关包

+ [django-gargoyle](https://github.com/disqus/gargoyle)
+ [django-waffle](https://github.com/jsocol/django-waffle)


## 受功能开关影响的单元测试代码

在测试代码中，应该对功能开关进行相应的开和关操作。

+ http://gargoyle.readthedocs.io/en/latest/usage/index.html#testing-switches
+ http://waffle.readthedocs.io/en/latest/testing/automated.html#testing-automated



 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
