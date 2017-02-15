---
title: Django REST 框架 V3 教程 2 - Request 和 Response
date: 2017-02-15
writing-time: 2017-02-15 19:27
categories: Programming
tags: Programming djangorestframework Django Python REST
---

# Request 对象

REST 框架中的 `Request` 类扩展至 Django 的 `HttpRequest`，它增强了对请求的解析功能。`Request.data` 类似于 `HttpRequest.POST`，但它对于 Web API 开发更加方便。

+ `HttpRequest.POST` 只能处理表单数据，只能在 POST 请求中使用。
+ `Request.data` 能处理任何数据，能在 POST, PUT, PATCH 请求中使用。


# Response 对象

REST 框架中的 `Response` 类扩展至 Django 的 `TemplateResponse`，它能根据客户端的要求返回不同的应答类型（即设置不同的 content type)。

# HTTP 返回状态代码

在 `status` 模块中定义了各种 HTTP 状态代码常量，如 `HTTP_400_BAD_REQUEST`。

# API 视图封装

REST 框架提供了 2 种封装器来方便我们开发 API 视图：

1. `@api_view` 装饰器：适用于 FBV。
2. `APIView` 类：适用于 CBV。

使用这些封装后，能确保我们的视图接收到的是 `Request` 实例，以及 `Response` 对象能根据客户要求返回不同的应答类型。它们还提供了一些异常处理功能，比如能处理 `405 Method Not Allowed` 异常，或者当访问错误格式的 `Request.data` 时处理 `ParseError` 异常。

# 代码重构

使用以上的这些新组件对 [Django REST 框架 V3 教程 1 - 序列化功能](http://www.atjiang.com/django-rest-tut1-serialization/) 中的 `views.py` 进行重构。由于使用了 `Response` 类，因此现在无需使用 `JSONResponse` 类了。

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer

# A view that supports listing all the existing snippets, or creating a new snippet.
@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new one.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# A view that corresponds to an individual snippet, can be used to
# retrieve, update or delete the snippet.
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

重构后，API 会根据客户的要求，返回不同的类型，例如，当用浏览器访问时，返回的是 HTML 格式的内容，而不是 JSON 的了。

# 在 URL 中加载可选的格式后缀

由于已经不再硬编码返回一种内容格式了，现在可进一步在 URL 上添加格式后缀，以明确返回要求的格式。带格式后缀的 URL 形如 `http://example.com/api/items/4.json`。

先在视图中加上 `format` 参数，如：

```python
def snippet_list(request, format=None):

def snippet_detail(request, pk, format=None):
```

现在稍微修改下 urls.py，将 urlpatterns 变为 format_suffix_patterns：

```python
# file: tutorial.snippets.urls.py
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

一般无需在 URL 上加格式后缀，但是添加后，就能更简单明晰地请求返回特定的格式了。

# 测试使用

可以同 [Django REST 框架 V3 教程 1 - 序列化功能](http://www.atjiang.com/django-rest-tut1-serialization/) 中的方法一样进行测试。

## 指定返回格式

通过 `Accept` 头指定：

```bash
$ http http://127.0.0.1:8000/snippets/snippets/ Accept:application/json

HTTP/1.0 200 OK
Allow: POST, OPTIONS, GET
Content-Type: application/json
Date: Wed, 15 Feb 2017 12:26:04 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "code": "foo = \"bar\"\n", 
        "id": 1, 
        "language": "python", 
        "linenos": false, 
        "style": "friendly", 
        "title": ""
    }, 
    {
        "code": "print \"hello, world\"\n", 
        "id": 2, 
        "language": "python", 
        "linenos": false, 
        "style": "friendly", 
        "title": ""
    }
]


$ http http://127.0.0.1:8000/snippets/snippets/ Accept:text/html # 返回 HTML
```

也可以通过格式后缀来访问：

```bash
$ http http://127.0.0.1:8000/snippets/snippets.json  # JSON suffix
$ http http://127.0.0.1:8000/snippets/snippets.api   # Browsable API suffix
```

# POST 请求

```bash
# POST using form data
$ http --form POST http://127.0.0.1:8000/snippets/snippets/ code="print 123"

{
  "id": 3,
  "title": "",
  "code": "print 123",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}

# POST using JSON
$ http --json POST http://127.0.0.1:8000/snippets/snippets/ code="print 456"

{
    "id": 4,
    "title": "",
    "code": "print 456",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

# 参考 

+ [Tutorial 2: Requests and Responses](http://www.django-rest-framework.org/tutorial/2-requests-and-responses/)
