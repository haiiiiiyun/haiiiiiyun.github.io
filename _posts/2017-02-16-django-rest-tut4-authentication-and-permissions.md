---
title: Django REST 框架 V3 教程 4 - 认证和权限
date: 2017-02-16
writing-time: 2017-02-16 08:44--10:22
categories: Programming
tags: Programming djangorestframework Django Python REST Authentication Permission
---

[Django REST 框架 V3 教程 3 - CBV](http://www.atjiang.com/django-rest-tut3-cbv/) 中实现的 API 没有任何权限管理。

本教程实现以下功能：

+ 代码段会与其创建者关联
+ 只有授权的用户才可能创建代码段
+ 只有创建者才能进行更新和删除
+ 未认证请求只能进行只读操作


# 在数据模型中添加内容

在 Snippet 数据模型中添加下面 2 项：

```python
# file: tutorial/snippets/models.py
#...
#class Snippet(..):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
#...
```

新增的 `owner` 项进来记录创建者，并且设置了反向关联名 `snippets`，这样，在 User 数据模型中就可以用 `User.snippets` 访问该用户创建的所有代码段数据了。

`highlighted` 项进来保存代码段的 HTML 高亮版本，它在每次数据模型调用 `.save()` 时会自动更新，因此要重载 Snippet 数据模型中的 `save()` 方法，如下：

```python
# file: tutorial/snippets/models.py
#...
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

#class Snippet(..):
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)
```

将更新同步到数据库：

```bash
$ python manage.py makemigrations snippets # 输入默认值
$ python manage.py migrate
$ python manage.py createsuperuser  # 创建更多的用户用以测试
```

# 为 User 数据模型添加 API

创建 UserSerializer：

```python
# file: tutorial/snippets/serializers.py
#...
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
```

因 `snippets` 是一个反向关联名，故在用 `ModelSerializer` 创建 UserSerializer 时默认不会包含该项，我们需要显式地添加。

为 User API 添加视图代码，因对 User 只进行只读操作，故只用了 ListAPIView 和 RetrieveAPIView：

```python
# file: tutorial/snippets/views.py
#...
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

添加 URL:

```python
# file: tutorial/snippets/urls.py
#...
url(r'^users/$', views.UserList.as_view()),
url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
```

# Snippet 记录与用户关联

重载 Snippet 视图的 `.perform_create` 方法，将 `request.user` 信息导入：

```python
# file: tutorial/snippets/views.py
#...
# class SnippetList(..):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

这样，Serializer 在调用 `.save()` 创建 Snippet 实例时，会传入一个额外的参数 `owner`。

# 更新 SnippetSerializer

将 owner 加入：

```python
# file: tutorial/snippets/serializers.py
#...
# class SnippetSerializer(..):
    owner = serializers.ReadOnlyField(source='owner.username')
    # ...
    class Meta:
        fields = ('owner', ...)
```

ReadOnlyField 中的 `source` 参数控制用哪个属性值作为该项的值来显示，它可以指向 Serializer 实现中的任何一个项上的任何一个属性，解析方法类似 Django 模板语言中的做法。它是一个无类型类，等同于 CharField(read_only=True)。

# 将所需权限添加到视图中

REST 框架内置了许多权限类，例如 `IsAuthenticatedOrReadOnly`，它能确保已认证的请求具有读写权限，而非认证请求只有只读权限。

```python
# file: tutorial/snippets/views.py
#...
from rest_framework import permissions

# class SnippetList:
    # ...
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class SnippetDetail:
    # ...
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
```

# 为 Browsable API 添加登录 URL

```python
# file: tutorial/urls.py
#...

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
```

确保添加了 `namespace='rest_framework'`，在 Django 1.9+ 中，REST 框架会自动设置该 namespace, 可以省略。

现在通过 `/snippets/users/` API 查看时，会看到每个用户信息中的 `snippets` 项，将列出该用户创建的所有 Snippet 的 ID 值。


# 对象级别的权限

创建一个自定义权限来实现只有创建者才能进行更新和删除操作。

```python
# file: tutorial/snippets/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permission are allowed to any request,
        # so we'll always allow GET, HEAD, OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        return obj.owner == request.user
```

在 SnippetDetail 中更新 permissions 属性：

```python
# file: tutorial/snippets/views.py
# ...
from .permissions import IsOwnerOrReadOnly
#class SnippetDetail(..)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
```

现在通过浏览器查看 Snippet 实现时，只有创建者才会看到 `DELETE` 和 `PUT` 操作按钮了。


# 认证设置

类似 APIView 中的 permission_classes 属性，也有一个 authentication_classes 用来设置认证类，如果没有设置，默认会使用 `(SessionAuthentication, BasicAuthentication)`。

当用浏览器查看时，Session 会包含认证信息。当通过 API 交互时，每个请求中都必须包含认证信息，如何未包含，就会出错：

```bash
$ http POST http://127.0.0.1:8000/snippets/snippets/ code="print 123" # 出错

HTTP/1.0 403 Forbidden
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Date: Thu, 16 Feb 2017 02:21:22 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "detail": "Authentication credentials were not provided."
}

$ http -a admin:password123 POST http://127.0.0.1:8000/snippets/snippets/ code="print 789"

HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Date: Thu, 16 Feb 2017 02:21:58 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "code": "print 789", 
    "id": 6, 
    "language": "python", 
    "linenos": false, 
    "owner": "admin", 
    "style": "friendly", 
    "title": ""
}
```

# 参考 

+ [Tutorial 4: Authentication and Permissions](http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)
