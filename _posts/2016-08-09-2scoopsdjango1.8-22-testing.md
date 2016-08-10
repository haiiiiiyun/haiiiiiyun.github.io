---
title: Django 项目测试
date: 2016-08-09
writing-time: 2016-08-09 16:32
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

处理生命财产安全的应用必须要测试。

相关包： coverage.py。

# 如何组织测试

为不同的组件创建单独的测试文件，不要全部放在 tests.py 中（该文件要删除），如：

```conf
popsicles/
    __init__.py
    admin.py
    forms.py
    models.py
    test_forms.py
    test_models.py
    test_views.py
    views.py
```

如上所示，测试模块名必须以 **test_** 开头

# 如何写单元测试

## 每个测试函数只测试一样事情

一个单元测试不应该对多个视图、数据模型、表单或者类中的多个方法的行为同时进行测试。它应该只对单个视图、数据模型、表单、函数或者方法进行测试。

当然，实际中各组件都会有关联，因此，针对一个特定的测试，应该构建一个绝对最小化的环境。例如：

```python
# flavors/test_api.py
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from flavors.models import Flavor

class FlavorAPITests(TestCase):

	def setUp(self):
		Flavor.objects.get_or_create(title="A Title", slug="a-slug")

def test_list(self):
	url = reverse("flavor_object_api")
	response = self.client.get(url)
	self.assertEquals(response.status_code, 200)
	data = json.loads(response.content)
	self.assertEquals(len(data), 1)
```

如上所示，我们使用 **setup()** 方法为该本次测试创建尽可能少的记录。

下面是一个较大的示例：

```python
# flavors/test_api.py
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from flavors.models import Flavor

class DjangoRestFrameworkTests(TestCase):

	def setUp(self):
		Flavor.objects.get_or_create(title="title1", slug="slug1")
		Flavor.objects.get_or_create(title="title2", slug="slug2")
		self.create_read_url = reverse("flavor_rest_api")
		self.read_update_delete_url = \
			reverse("flavor_rest_api", kwargs={"slug": "slug1"})

	def test_list(self):
		response = self.client.get(self.create_read_url)

		# Are both titles in the content?
		self.assertContains(response, "title1")
		self.assertContains(response, "title2")

	def test_detail(self):
		response = self.client.get(self.read_update_delete_url)
		data = json.loads(response.content)
		content = {"id": 1, "title": "title1", "slug": "slug1",
										"scoops_remaining": 0}
		self.assertEquals(data, content)

	def test_create(self):
		post = {"title": "title3", "slug": "slug3"}
		response = self.client.post(self.create_read_url, post)
		data = json.loads(response.content)
		self.assertEquals(response.status_code, 201)
		content = {"id": 3, "title": "title3", "slug": "slug3",
											"scoops_remaining": 0}
		self.assertEquals(data, content)
		self.assertEquals(Flavor.objects.count(), 3)

	def test_delete(self):
		response = self.client.delete(self.read_update_delete_url)
		self.assertEquals(response.status_code, 204)
		self.assertEquals(Flavor.objects.count(), 1)
```

## 测试视图中，尽可能用 Request Factory

**django.test.client.RequestFactory** 可以创建一个可作为视图第一个参数的 reqeust 实例。这种实例比标准 Django 测试客户端更具隔离性。但是由于它不支持中间件（包括会话和认证功能），因此在编写测试代码时需要多做一些工作。

举例来说，假设要对一个经过中间件类处理过的视图进行测试（如需要会话功能），可以如下处理：

```python
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from .views import cheese_flavors

def add_middleware_to_request(request, middleware_class):
	middleware = middleware_class()
	middleware.process_request(request)
	return request

def add_middleware_to_response(request, middleware_class):
	middleware = middleware_class()
	middleware.process_request(request
	return request

class SavoryIceCreamTest(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()

	def test_cheese_flavors(self):
		request = self.factory.get('/cheesy/broccoli/')
		request.user = AnonymousUser()

		# Annotate the request object with a session
		request = add_middleware_to_request(request, SessionMiddleware)
		request.session.save()

		# process and test the request
		response = cheese_flavors(request)
		self.assertContains(response, "bleah!")
```

## 不要写需要测试的测试代码

测试代码必须尽量简单明了。

## 编写测试时不适用 DRY

当需要类似但不同数据的测试方法时，可以对代码复制粘贴，然后传递不同的参数。

## 不要依赖 Fixture

使用 Fixture 问题多多，它难以维护，难以跟踪项目数据的更新。

能用于创建测试数据的一些库：

+ factory boy
+ model mommy
+ mock

## 需要测试的东西

尽可能测试所有东西！

视图： 数据的呈现、数据的修改、自定义的 CBV 方法。
数据模型： 数据模型的创建/更新/删除，数据模型的方法，模型管理器的方法。
表单：表单方法，clean()、自定义项。
验证器：对每一个自定义的验证器编写多个测试方法，确保这些验证器不会对网站数据造成破坏。
信号：由于它们的作用比较直接，不进行测试可能会引起困惑。
过滤器：由于它们本质是函数，故测试应该较容易。
模板 Tag：由于它们能完成任何功能，并且可以接受模板上下文对象，对它们进行测试非常有难度。这也意味着需要对它们进行测试，因为可以不测试可以会存在边界条件问题。

项目中不需要测试的部分是那些已经在 Django 核心包或者第三方包中已经测试过的那部分。










> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
