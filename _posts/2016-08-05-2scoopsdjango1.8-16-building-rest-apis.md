---
title: Django 创建 REST API
date: 2016-08-08
writing-time: 2016-08-05 13:42--2016-08-08 11:34
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
更新一个现有资源的部分内容          | PATCH     | UPDATE
删除一个资源                        | DELETE    | DELETE
返回某个 URL 所支持的 HTTP 方法     | OPTIONS   |
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

HTTP 状态码            | 成功/失败 | 含义
-----------------------|-----------|
200 OK                 | 成功      | GET-返回资源;PUT-返回状态消息或返回资源
201 Created            | 成功      | POST-返回状态消息或返回新建的资源
204 No Content         | 成功      | DELETE-对删除请求的成功完成的应答
304 Unchanged          | 转向      | 表示自上次请求以来无改动。用于检查 Last-Modified 和 Etag 以提高性能
400 Bad Request        | 失败      | 返回错误消息，包括表单验证错误
401 Unauthorized       | 失败      | 请求需要认证，但用户未提供相关信息
403 Forbidden          | 失败      | 企图访问受限内容
404 Not Found          | 失败      | 资源未找到
405 Method Not Allowed | 失败      | 企图使用未允许的 HTTP 方法
410 Gone               | 失败      | 企图使用一个不再支持的方法。用于当新版本 API 发布而旧版本关闭时。移动应用需对它进行测试，并提醒用户升级
429 Too Many Request   | 失败      | 用户在某时段内请求次数过多。

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

这种组织方式下，API 应用会变得越来越大，并且每个 API 与原应用的关联会越来越疏远。

## 实现应用功能的代码应该位于应用目录内

REST API 本质是视图。对于简单小型的项目，这些 API 视图应该位于 *views.py* 或 *viewsets.py* 中，并且遵循视图的实现指南（尽量不含业务逻辑）。对于有太多 REST API 类的大型项目，应将这些视图移到新的模块 *viewset* 下。

这些组织方式下，如果有很多的关联小应用，对于 API 组件到底在哪个应用中实现会比较难找。

## 和普通视图一样，尽量不要在 API 视图中放业务逻辑

## API URL 分组

如果 REST API 视图分布在不同的应用中，如何创建如下的项目级的 API 布局？

```conf
api/flavors/ # GET, POST
api/flavors/:slug/ # GET, PUT, DELETE
api/users/ # GET, POST
api/users/:slug/ # GET, PUT, DELETE
```

以前，我们将所有的 API 视图代码都放在一个专门的应用中，如 **api** 或 **apiv1**。理论上来说这种方法不错，但实际上会有重复的代码存在。

而现在的方法是更依赖 URL 配置文件。当创建项目级的 API 时，先将 REST 视图的内容写在 **views.py** 或 **viewsets.py** 中，然后在 URLConf 中（如 **core/api.py** 或 **core/apiv1.py**）中进行关联，最后在根 **urls.py** 中包含进来。实现方式如下：

```python
"""Called from the project root's urls.py URLConf thus:
		url(r"ˆapi/", include("core.api", namespace="api")),
"""
from django.conf.urls import url

from flavors import views as flavor_views
from users import views as user_views

urlpatterns = [
	url(
		regex=r"ˆflavors/$",
		view=flavor_views.FlavorCreateReadView.as_view(),
		name="flavors"
	),
	url(
		regex=r"ˆflavors/(?P<slug>[-\w]+)/$",
		view=flavor_views.FlavorReadUpdateDeleteView.as_view(),
		name="flavors"
	),
	url(
		regex=r"ˆusers/$",
		view=user_views.UserCreateReadView.as_view(),
		name="users"
	),
	url(
		regex=r"users/(?P<slug>[-\w]+)/$",
		view=user_views.UserReadUpdateDeleteView.as_view(),
		name="users"
	),
]
```

## 要对 API 进行测试

## 要对 API 进行版本控制

API URL 要有版本信息，如 **/api/v1/flavors** ，**/api/v1/users**，然后当 API 有修改后，变成 **api/v2/flavors**， **/api/v2/users**。这样，当版本号升级后，原有用户就可以继续使用之前的 API。

同时，对旧版本 API 的支持很有必要，对过时 API 支持几个月很常见。

当实现一个 API 时，给用户提供过时警告信息和足够的时间，使他们能有时间完成升级。从个人经验来说，能向用户发送过时警告信息是请求收集用户邮件地址的最好理由。


# 面向服务的体系结构 SOA

SOA 型的 Web 应用会拆分成一个个相互独立的组件。每个组件可能会运行于各自独立的服务器上，各组件间通常是通过 REST API 进行交互的。

采用 SOA 方式的主要原因是为使开发人员更易独立开发不同组件。不同于 100 个开发人员一起开始同一个功能，可以将他们分成 10 人一组，各组开发各自独立的 SOA 组件。

但是对于小项目，SOA 弊大小利，过多的组件会增加系统的复杂度。

要想实现一个 SOA 型的 Web 应用，先按常规进行开发，然后随着业务的发展，将 Web 应用中的每个应用发展成一个个独立的 SOA 组件。

# 如何关闭对外公开的 API

## 第 1 步：预告通知用户

尽早通知。最好提升 6 个 月，最少要有 1 个月。通过电子邮件、 blog 和社交媒体通知 API 用户。通知次数越多越好。

## 第 2 步：使该 API 返回 410 错误

最终关闭后，将该 API 改为返回 410 错误，内容包括：

+ 一个到新的 API 端点的链接
+ 一个到新的 API 文档的链接
+ 一个为何要关闭的详情页的链接

以下是关闭后返回 410 错误页的示例：

```python
# core/apiv1_shutdown.py
from django.http import HttpResponseGone

apiv1_gone_msg = """APIv1 was removed on April 2, 2015. Please switch to APIv3:
<ul>
	<li>
		<a href="https://www.example.com/api/v3/">APIv3 Endpoint</a>
	</li>
	<li>
		<a href="https://example.com/apiv3_docs/">APIv3 Documentation</a>
	</li>
	<li>
		<a href="http://example.com/apiv1_shutdown/">APIv1 shut down notice</a>
	</li>
</ul>
"""

def apiv1_gone(request):
	return HttpResponseGone(apiv1_gone_msg)
```

# REST 框架评估

## django-rest-framework 是事实上的标准包

采用该包更能保证以后能获得维护，且更易找到开发人员。

## REST API 比 RPC 更易实现

## 推荐用 CBV

# 访问 API 的速率限制

需要对用户在特定的一段时间内对某一 API 能进行多少次请求进行限制。

## 没有限制的 API 访问很危险，可能会拖垮系统

## REST 框架系统要有速率限制功能

## 可以将速率限制考虑到商业计划中

假如有一个上传图片的 API, 可以针对不同用户这样定价：

+ 开发人员：免费，但只允许在 1 小时内进行 10 次 API 请求
+ 基本： $24/月，允许 1 分钟内进行 25 次请求
+ 高级： $79/月, 允许 1 分钟内进行 50 次请求
+ 企业： $5000/月，允许 1 分钟内进行 200 次请求


# 推广 REST API

## 文档

提供完整的文档很重要，最好通俗易懂。必须要有易用的示例代码。

## 向客户提供 SDK

为不同的编程语言提供 SDK，包括的语言越多越好。必须包括的语言有： Python、JavaScript、Ruby、PHP、Go 和 Java。

一般自己先用至少以上一种语言实现库和一个示例项目。这不仅有助于推广，而且还能从用户角度对 API 进行省视。

# 推荐资源：

+ [REST WORST PRACTICES](https://jacobian.org/writing/rest-worst-practices/)


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
