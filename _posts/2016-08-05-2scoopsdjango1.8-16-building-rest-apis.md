---
title: Django 创建 REST API
date: 2016-08-05
writing-time: 2016-08-05 13:42
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

#  REST API 设计基础

REST API 操作与 HTTP 方法的关系

请求目的                            | HTTP 方法 | 相应的 SQL
------------------------------------|-----------|
创建一个资源                        | POST      | INSERT
读取一个现有资源                    | GET       | SELECT
请求现有资源的元数据                | HEAD      |
更新一个现有资源                    | PUT       | UPDATE
更新一个现有资源的部分内部          | PATCH     | UPDATE
删除一个资源                        | DELETE    | DELETE
返回对于某个 URL 所支持的 HTTP 方法 | OPTIONS   |
请求回响                            | TRACE     |
TCP/IP 隧道（一般都未实现）         | CONNECT   |


注意事项：

+ 如果想实现一个只读 API，只需实现 GET 方法即可
+ 如果想实现一个可读写的 API，则必须至少实现 POST，但应该考虑用 PUT 和 DELETE
+ 为简单起见，REST API 架构通常只使用 GET 和 POST
+ 按照定义，GET、PUT 和 DELETE 是幂等的，但是 POST 和 PATCH 不是
+ 通常不实现 PATCH，但是如果 API 支持 PUT，则最好实现 PATCH
+ django-rest-framework 和 django-tastypie 都考虑了以上的所有问题


REST API 使用到的一些 HTTP 状态码及其含义：

HTTP 状态码 | 成功/失败 | 含义
200 | x |x
200 OK | 成功| GET-返回资源;PUT-返回状态消息或返回资源
201 Created | 成功 | POST-返回状态消息或返回新建的资源
204 No Content | 成功 | DELETE-对删除请求的成功完成的应答
304 Unchanged | 转向 | 表示自上次请求以来无改动。用于检查 Last-Modified 和 Etag 以提高性能
400 Bad Request | 失败 | 返回错误消息，包括表单验证错误
401 Unauthorized | 失败 | 请求需要认证，但是用户未提供相关信息
403 Forbidden | 失败 | 企图访问受限内容
404 Not Found | 失败 | 资源未找到
405 Method Not Allowed | 失败| 企图使用未允许的 HTTP 方法
410 Gone | 失败 | 企图使用一个不再支持的方法。用于当新版本 API 发布而旧版本关闭时。移动应用要对些进行测试，并提供用户升级
429 Too Many Request | 失败 | 用户在某时段内请求次数过多。

# 使用 django-rest-framework 实现一个简单的 JSON API

数据模型：

```python

# flavors/models.py
from django.core.urlresolvers import reverse
from django.db import models

class Flavor(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	scoops_remaining = models.IntegerField(default=0)

	def get_absolute_url(self):
		return reverse("flavors:detail", kwargs={"slug": self.slug})
```

定义序列化器：

```python
from rest_framework import serializers

from .models import flavor

class FlavorSerializer(serializers.ModelSerializer):
	class Meta:
		model = flavor
		fields = ('title', 'slug', 'scoops_remaining')
```

定义视图：

```python
# flavors/views
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetriveUpdateDestroyAPIView
from .models import Flavor
from .serializers import FlavorSerializer

class FlavorCreateReadView(ListCreateAPIView):
	queryset = Flavor.objects.all()
	serializer_class = FlavorSerializer
	lookup_field = 'slug'

class FlavorReadUpdateDeleteView(RetriveUpdateDestroyAPIView):
	queryset = Flavor.objects.all()
	serializer_class = FlavorSerializer
	lookup_field = 'slug'
```

使用 Django REST 框架时，可以参考 [cdrf.co](http://cdrf.co),  上面列出了该框架所有方法与属性的详细说明。
	
将视图与 URL 关联：

```python
# flavors/urls.py
from django.conf.urls import url

from flavors import views

urlpatterns = [
	url(
		regex=r"^api/$",
		view=views.FlavorCreateReadView.as_view(),
		name="flavor_rest_api"
	),
	url(
		regex=r"^api/(?P<slug>[-\w]+)/$",
		view=views.FlavorReadUpdateDeleteView.as_view(),
		name="flavor_rest_api"
	),
]
```

这里，两个视图使用了相同的 URL 名，以便于前端使用。

URL 与 视图的关系表：

URL                 | 视图                       | URL 名（相同）
--------------------|----------------------------|
/flavors/api/       | FlavorCreateReadView       | flavor_rest_api
/flavors/api/:slug/ | FlavorReadUpdateDeleteView | flavor_rest_api

实现认证和权限控制参考：

+ [django-rest-framework authentication](http://www.django-rest-framework.org/api-guide/authentication/)
+ [django-rest-framework permission](http://www.django-rest-framework.org/api-guide/permissions/)

# REST API 架构

## 代码的组织应该整洁

对于一个包含多个相互关联的小应用的项目，很难确定应该将 API 视图放于何处。相比于将 API 代码分散在各个应用代码中，有时为 API 创建一个新的特定应用可能更合理。当然，应用名也应该体现出 API 的版本，例如 *apiv4*。

这种组织方式下，API 应用会越得越来越大，并且每个 API 与原应用的关联会越来越疏远。

## 实现应用功能的代码应该位于应用目录内

REST API 本质是视图。对于简单小型的项目，这些 API 视图应该位于 *views.py* 或 *viewsets.py* 中，并且遵循视图的实现指南（尽量不含业务逻辑）。对于有太多 REST API 类的大型项目，应将这些视图移到新的模块 *viewset* 下。

这些组织方式下，如果有很多的关联小应用，对于 API 组件到底在哪个应用中实现会比较难找。

## 可普通视图一样，尽量不要在 API 视图中放业务逻辑

## 















> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
