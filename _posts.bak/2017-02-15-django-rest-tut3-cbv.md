---
title: Django REST 框架 V3 教程 3 - CBV
date: 2017-02-15
writing-time: 2017-02-15 21:26--22:06
categories: Programming
tags: Programming djangorestframework Django Python REST CBV
---

使用 CBV 来开发 API，能够重用代码。

# 使用 CBV 重构视图

将 [Django REST 框架 V3 教程 2 - Request 和 Response](http://www.atjiang.com/django-rest-tut2-requests-and-responses/) 中的视图代码重构：

```python
# file: tutorial/snippets/views.py
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Snippet
from .serializers import SnippetSerializer

# A view that supports listing all the existing snippets, or creating a new snippet.
class SnippetList(APIView):
    """
    List all code snippets, or create a new one.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# A view that corresponds to an individual snippet, can be used to
# retrieve, update or delete the snippet.
class SnippetDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

使用 CBV 后，最大的特点是减少了对请求方法 `request.method` 的条件判断，将 REST 的操作对应的各种请求方法的处理都封装在了各自的类方法中。

使用 CBV 后，urls.py 也要进行相应调整：

```python
# file: tutorial/snippets/urls.py
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

重构后，项目应该也能和以前一样正常运行。

# 使用 Mixin

采用 CBV 后，我们能够容易地组合可重用的代码（即 Mixin)。由于针对每个数据模型，其 create/retrieve/update/delete 操作对应的 API 视图实现都非常类似，故 REST 框架已经将它们封装成了相应的 Minxin，以方便重用。

```python
#file: tutorial/snippets/views.py
from rest_framework import mixins
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer

# A view that supports listing all the existing snippets, or creating a new snippet.
class SnippetList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    List all code snippets, or create a new one.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# A view that corresponds to an individual snippet, can be used to
# retrieve, update or delete the snippet.
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

这里，`GenericAPIView` 定义了 REST 各种操作对应的默认实现，如 get, post, put, delete 等。

`ListModelMixin` 实现了 `.list()`，`CreateModelMixin` 实现了 `.create()`，`RetrieveModelMixin` 实现了 `.retrieve()`，`UpdateModelMixin` 实现了 `.update()`，`DestroyModelMixin` 实现了 `.destroy()`。

重构后，项目应该能和以前一样正常运行。

# 使用通用的 CBV 进行重构

REST 框架已经内置了一些通用的视图，这些视图已经将上面提到的相关 Mixin 功能都封装起来了，因此，使用这些通用视图进行重构，能进一步减少代码量：

```python
# file: tutorial/snippets/views.py
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer

# A view that supports listing all the existing snippets, or creating a new snippet.
class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new one.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

# A view that corresponds to an individual snippet, can be used to
# retrieve, update or delete the snippet.
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

重构后，代码相当的简洁。

# 参考 

+ [Tutorial 3: Class-based Views](http://www.django-rest-framework.org/tutorial/3-class-based-views/)
