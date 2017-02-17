---
title: Django REST 框架 V3 教程 5 - 超链接关联的 API
date: 2017-02-16
writing-time: 2017-02-16 11:34--16:00
categories: Programming
tags: Programming djangorestframework Django Python REST
---

本教程到目前为止，API 中各实体的关联都是通过主键处理的。为提高易用性，实现用超链接来表示关联。

#  为 Snippet.highlighted 属性创建 API

Snippet.highlighted 属性值是该代码段的高亮表示的 HTML 代码，因此我们不想让其 API 返回的是 JSON 格式，而要 HTML 格式。

REST 框架处理 HTML 格式有两种方式，1 种是通过模板来呈现 HTML，另 1 种是处理预编码了的 HTML 代码。本 API 采用后一种方式。

由于 Snippet.highlighted 是一个实例的属性，不是一个数据模型的实例，故没有现存的通用视图可以采用，只能使用 `generics.GenericAPIView`，然后实现 `.get()`：

```python
# file: tutorial/snippets/views.py
from rest_framework import renderers
from rest_framework.response import Response

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer, )

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
```

添加 URL：

```python
# file: tutorial/snippets/urls.py
# ...
url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
```

# 超链接关联

正确处理各实体间的关联性是 Web API 设计工作中的难点。一般可用以下几种方法来表示关联性：

+ 使用主键
+ 实体间使用超链接
+ 使用关联实体上的一个唯一标识的 slug 域
+ 使用关联实体的默认字符串表示
+ 将关联的实体放在父实体内
+ 其它自定义方式


REST 框架支持所有这些方法来表示关联。本例采用超链接来表示实体间的关联性。实现方法是将 SnippetSerializer 的基类从 `ModelSerializer` 改为 `HyperlinkedModelSerializer`。

`HyperlinkedModelSerializer` 与 `ModelSerializer` 的区别有：

+ 它默认不包含 `id` 项
+ 它包含有 `url` 项，类型为 HyperlinkedIdentityField
+ 关联性不使用 PrimaryKeyRelatedField，而用 HyperlinkedIdentityField 实现


重构 Serializer 以实现超链接关联：

```python
# file: tutorial/snippets/serializers.py
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                'title', 'code', 'linenos', 'language', 'style',)



class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedIdentityField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets',)
```

由于使用了 HyperlinkedModelSerializer，故默认不会包含 `id` 项，同时定义了一个新的 `url` 项。

HyperlinkedIdentityField 中的 `view_name` 参数指定了该超链接项的 URL，其值通过 `reverse()` 函数解析，因此这里用到的 `snippet-detail`, `snippet-highlight` 等 URL 名都必须在 urls.py 中定义。

对于数据模型的 Serializer，其默认的 `url` 项对应的 HyperlinkedIdentityField 的 view_name 值为 `数据模型名-detail`，例如 SnippetSerializer 对应 snippet-detail。

由上面的使用情况可看出，HyperlinkedIdentityField 的 view_name 参数对应的视图，都接收一个 pk 参数，以指出针对的是哪个具体的数据实例。

由于 URL 中都已加入了格式后缀，因此在 `highlight` 项定义中通过 `format='html'` 限制该超链接返回的是 HTML 格式。

# 命名 URL

```python
#file: tutorial/snippets/urls.py
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

# 添加分页功能

由于返回的记录可能很多，故需加上分页功能。

```python
#file: tutorial/settings.py
#...
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}
```

分页的详细讲解见 [Pagination](http://www.django-rest-framework.org/api-guide/pagination/)。

对于 `LimitOffsetPagination` 分页，请求格式为 `GET https://api.example.org/accounts/?limit=100&offset=400`，返回格式为：

```json
{
    "count": 1023, //数据库中的总记录数
    "next": "https://api.example.org/accounts/?limit=100&offset=500",
    "previous": "https://api.example.org/accounts/?limit=100&offset=300",
    "results": [
       …
    ]
}
```

# 创建根 API

该 API 将列出 `snippets` 和 `users` 的 API 链接，我们用 FBV 来实现：

```python
#file: tutorial/snippets/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET',])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })
```

这里用的是 REST 框架中的 `reverse` 方法，不是 Django 内置的版本，以便生成更加完整的 URL。

添加 URL：

```python
#file: tutorial/snippets/urls.py
url(r'^$', views.api_root),
```

# 测试使用

可以从 http://127.0.0.1:8000/snippets/ 根 URL 开始测试。



# 参考 

+ [Tutorial 5: Relationships &amp; Hyperlinked APIs](http://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/)
