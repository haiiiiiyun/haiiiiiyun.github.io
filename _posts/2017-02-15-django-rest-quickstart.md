---
title: Django REST 框架 V3 Quickstart
date: 2017-02-15
writing-time: 2017-02-15 08:55--11:30
categories: Programming
tags: Programming djangorestframework Django Python REST
---

# 概述

Django REST 框架是一个功能强大易用的 Web API 创建工具集。

其有如下特性：

+ 对开发人员友好的 Web browsable API
+ 支持 OAuth1a 和 OAuth2 等认证
+ 支持对 ORM 和非 ORM 数据源的序列化


# 依赖

## 必要依赖

+ Python 2.7, 3.2+
+ Django 1.8+


## 可选依赖

+ [coreapi](http://pypi.python.org/pypi/coreapi/)(1.32.0+) - 支持 Schema 创建
+ [Markdown](http://pypi.python.org/pypi/Markdown/)(2.1.0+) - browsable API 的 Markdown 支持
+ [django-filter](http://pypi.python.org/pypi/django-filter)(0.9.2+) - 过滤支持
+ [django-crispy-forms](https://github.com/maraujop/django-crispy-forms) - 对 HTML 元素的增强显示
+ [django-guardian](https://github.com/lukaszb/django-guardian)(1.1.1+) - 对象级别的权限支持


# Quickstart 示例项目

该项目可使管理员通过 API 查看和编辑用户和组信息。

## 项目设置

创建一个新项目 `tutorial`，并开启一个 quickstart 应用：

```bash
$ mkdir django-rest-framework-v3 # 测试项目的基目录
$ cd django-rest-framework-v3

# 创建 virtualenv wrapper env
$ mkvirtualenv env 
$ workon env

# 安装依赖包
$ pip install django==1.10.5
$ pip install djangorestframework==3.5.4

# 在当前目录下创建新项目
$ django-admin.py startproject tutorial ./
$ cd tutorial/tutorial
$ django-admin.py startapp quickstart
$ cd ..

$ python manage.py migrate

# 创建一个初始管理员 admin:password123
$ python manage.py createsuperuser
```

## Serializers

创建 User 和 Group 的 Serializer, 它类似 Model Form 的创建：

```python
# file: tutorial/quickstart/serializers.py
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
```

这里使用了超链接关系。还可以使用主键及其它关联。

## Views

ViewSet 集成了 REST 常用操作对应的 View。

```python
# file: tutorial/quickstart/views.py
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('-date_joined')
    serializer_class = GroupSerializer
```

## URLs

由于使用了 ViewSet，REST 操作对应的 URL 配置信息可以直接提取出来：

```python
# file: tutorial/urls.py
from django.conf.urls import url, include
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), # browsable API 的 login URL
]
```

## Settings

```python
#file: tutorial/settings.py
INSTALLED_APPS = (
    # ...,
    'rest_framework',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASS': [
        'rest_framework.permissions.IsAdminUser', # 只允许管理员访问 API
    ],
    'PAGE_SIZE': 10 # 开启分页
}
```

## 测试使用 API

```bash
$ python manager.py runserver # 开启服务
```

用 `curl` 命令测试：

```bash
$ curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin",
            "email": "admin@example.com",
            "groups": []
        }
    ]
```

用 [httpie](https://github.com/jakubroztocil/httpie#installation) 命令测试：

```bash
$ http -a admin:password123 http://127.0.0.1:8000/users/
HTTP/1.0 200 OK
Allow: GET, POST, OPTIONS
Content-Type: application/json
Date: Wed, 15 Feb 2017 03:25:35 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "count": 2, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "email": "hy@example.com", 
            "groups": [], 
            "url": "http://127.0.0.1:8000/users/2/", 
            "username": "hy"
        }, 
        {
            "email": "admin@example.com", 
            "groups": [], 
            "url": "http://127.0.0.1:8000/users/1/", 
            "username": "admin"
        }
    ]
}
```

或者直接通过浏览器访问 http://127.0.0.1:8000/users/。


# 参考 

+ [Django REST Framework Homepage](http://www.django-rest-framework.org/)
+ [Django REST Framework Quickstart](http://www.django-rest-framework.org/tutorial/quickstart/)
