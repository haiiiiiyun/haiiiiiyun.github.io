---
title: Django REST 框架 V3 教程 6 - ViewSet 和 Router
date: 2017-02-17
writing-time: 2017-02-17 08:51--10:44
categories: Programming
tags: Programming djangorestframework Django Python REST
---

REST 框架中的 `ViewSet` 非常类似 `View`，它基于一些常用约定，实现了 list, create, retrieve, update, partial_update, destroy 等方法。

`ViewSet` 在最后的实例化时，才会将 list, create 等方法绑定到 get, post, put, patch, delete 等 REST 操作对应的处理函数（通常由 `Router` 创建 URL 定义时自动绑定），最后绑定到 model-list, model-create, model-detail 等 URL。

# 使用 ViewSet 进行重构

将 UserList 和 UserDetail 视图重构到一个 UserViewSet 中：

```python
#file: tutorial/snippets/views.py
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

ReadOnlyModelViewSet 实现了只读的操作，如 list, detail 等。

接着将 SnippetList, SnippetDetail SnippetHighlight 重构到一个 SnippetViewSet 中：

```python
#file: tutorial/snippets/views.py
from rest_framework.decorators import detail_route

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                    IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer,])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

这里使用了 ModelViewSet，从而实现了默认的读写操作方法。

要实现一个自定义的操作，比如 `highlight`，需要为其定义一个方法，并且加上装饰器 `@detail_route`。该装饰器可用在所有非标准 `create/update/delete` 风格的自定义 API 上。

使用了 `@detail_route` 的自定义方法的 API 默认只响应 GET 请求，如果要响应 POST 等请求，需要在装饰器的 `methods` 参数中指定。自定义方法的 API，其 URL 默认就是函数名本身，如 highlight，要想修改，需要在 `@detail_route` 装饰器的 `url_path` 参数中指定。

# 手动将 ViewSet 绑定到 URL

通过手动将 ViewSet 转成具体的 View，以了解 ViewSet 的工作原理。

```python
#file: tutorial/snippets/urls.py
from .views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'^$', api_root),
    url(r'^snippets/$',
        snippet_list,
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        snippet_detail,
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        snippet_highlight,
        name='snippet-highlight'),
    url(r'^users/$',
        user_list,
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        user_detail,
        name='user-detail'),
]
```

现在，系统应该能和之前一样正常运行。

# 使用 Router 进一步重构

将 ViewSet 自动转成具体的 View 并绑定到 URL 的操作可以由 Router 自动完成。

```python
#file: tutorial/snippets/urls.py
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls)),
]
```

Router 还自动生成了 api_root，并为 URL 加上了后缀功能，从而无需定义 api_view 视图及使用 format_suffix_patterns 了。


# 参考 

+ [Tutorial 6: ViewSets &amp; Routers](http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/)
