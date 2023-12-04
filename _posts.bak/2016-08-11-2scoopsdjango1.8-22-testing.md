---
title: Django 项目测试
date: 2016-08-11
writing-time: 2016-08-09 16:32--2016-08-11 10:05
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

生命财产安全相关的应用必须要测试。

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

如上所示，我们使用 **setup()** 方法为本次测试创建尽可能少的记录。

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

可创建测试数据的一些库：

+ factory boy
+ model mommy
+ mock

## 需要测试的东西

尽可能测试所有东西！

视图： 数据的呈现、数据的修改、自定义的 CBV 方法。
数据模型： 数据模型的创建/更新/删除，数据模型的方法，模型管理器的方法。
表单：表单方法，clean()、自定义项。
验证器：对每一个自定义的验证器编写多个测试方法，确保这些验证器不会对网站数据造成破坏。
信号：由于它们的作用比较间接，不进行测试可能会引起困惑。
过滤器：由于它们本质是函数，故测试应该较容易。
模板 Tag：由于它们能完成任何功能，并且可以接受模板上下文对象，对它们进行测试非常有难度。这也意味着需要对它们进行测试，因为如果不测试可能会存在边界条件问题。

项目中不需要测试的部分是那些已经在 Django 核心包或者第三方包中已经测试过的那部分。

## 测试失败的情况比测试成功的情况更重要

## 通过 Mock 使得单元测试不与外界交互

单元测试不应该测试本函数或方法以外的事物。因此在测试过程中不应该访问外部的 API、接收邮件、调用挂钩等。但是要测试的函数很可能会包含外部 API，此时有两种可选方法：

+ 一、将单元测试变成集成测试
+ 二、使用 Mock 库来模拟外部 API 应答

使用 Mock 库能非常容易地将某库的功能进行临时修改，从而使它们能返回我们想到的数据。

下面的例子中， Mock 对 icecreamapi 模块中的对象进行了修改：

```python
import mock
import unittest

import icecreamapi

from flavors.exceptions import CantListFlavors
from flavors.utils import list_flavors_sorted

class TestIceCreamSorting(unittest.TestCase):

	# Set up monkeypatch of icecreamapi.get_flavors()
	@mock.patch.object(icecreamapi, "get_flavors")
	def test_flavor_sort(self, get_flavors):
		# Instructs icecreamapi.get_flavors() to return an unordered list.
		get_flavors.return_value = ['chocolate', 'vanilla', 'strawberry', ]

		# list_flavors_sorted() calls the icecreamapi.get_flavors()
		# function. Since we've monkeypatched the function, it will always
		# return ['chocolate', 'strawberry', 'vanilla', ]. Which the.
		# list_flavors_sorted() will sort alphabetically
		flavors = list_flavors_sorted()

		self.assertEqual(
			flavors,
			['chocolate', 'strawberry', 'vanilla', ]
		)
```

下面是测试失败情况下的代码：

```python
@mock.patch.object(icecreamapi, "get_flavors")
def test_flavor_sort_failure(self, get_flavors):
	# Instructs icecreamapi.get_flavors() to throw a FlavorError.
	get_flavors.side_effect = icecreamapi.FlavorError()

	# list_flavors_sorted() catches the icecreamapi.FlavorError()
	# and passes on a CantListFlavors exception.
	with self.assertRaises(CantListFlavors):
		list_flavors_sorted()
```

下面是对 python requests 连接进行修改的例子：

```python
@mock.patch.object(requests, "get")
def test_request_failure(self, get)
	"""Test if the target site is innaccessible."""
	get.side_effect = requests.exception.ConnectionError()

	with self.assertRaises(CantListFlavors):
		list_flavors_sorted()

@mock.patch.object(requests, "get")
def test_request_failure(self, get)
	"""Test if we can handle SSL problems elegantly."""
	get.side_effect = requests.exception.SSLError()

	with self.assertRaises(CantListFlavors):
		list_flavors_sorted()
```

## 使用功能更强的断言方法

假如要比较两个列表，如果用 assertEqual，那么需要先对列表进行相同的排序操作，然后才能进行比较，而使用 unittests.ListItemsEqual() 则不用这么麻烦。

以下是比较有用的断言方法：

+ assertRaises()
+ Python 2.7: ListItemsEqual(), Python 3+ assertCountEqual()
+ assertDictEqual()
+ assertFormError()
+ assertContains() 先检测状态 200，然后再检查 response.content
+ assertHTMLEqual() 忽略空白符的不同
+ assertJSONEqual()

更多参考：
[python2 assert-methods](https://docs.python.org/2/library/unittest.html#assert-methods)
[python3 assert-methods](https://docs.python.org/3/library/unittest.html#assert-methods)
[django assertions](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#assertions)

## 对每个测试都要写明测试目的文档

即便是小小的 docstring 也能帮很大的忙。

# 集成测试

集成测试是将单独的模块组合成一个整体进行测试，它在单元测试之后进行。集成测试的例子有：

+ 使用 Selenium 测试应用是否能在浏览器中正确运行
+ 与第三方 API 进行真实测试
+ 与 [requestb.in](http://requestb.in/) 或 [httpbin](http://httpbin.org/) 交互来确认出站请求的有效性
+ 使用 [runscope.com](https://www.runscope.com/) 来确保 API 能正常运行

集成测试的缺点：

+ 设置集成测试要花很多时间
+ 运行速度非常慢。因此它是对整个系统进行测试
+ 有错误抛出时，很难定位。例如，一个只对某类浏览器有影响的错误可能是由数据库层的 Unicode 转换引起的
+ 相比单元测试更脆弱。某个组件中的一个小修改都可能会破坏它。

# 持续集成

对于任何大小的项目，都应该设置一个持续集成 CI 服务器，对提交后的项目进行测试。

# 测试的必要性

> Tests are the Programmer's stone, transmuting fear into boredom." -Kent Beck

测试虽然花时间，但是在处理升级时非常有用，因此花的时间是非常值得的。

当进行升级时：

+ 先在本地升级相关包或库
+ 运行测试
+ 修正测试过程中抛出的所有错误
+ 再进行一些手工检查

如果没有测试，每次升级时，都要对所有的使用情景进行一次次的手工操作测试。

# 测试覆盖的游戏

测试覆盖度即是对开发人员进行督促的工具，也是用来评估项目状态的度量。

# 设置覆盖测试

我们只需对自己的代码进行测试，不对 Django 和第三方包进行测试。

## 开始编写测试

## 运行测试并生成覆盖报告

在 &lt;project_root&gt; 目录下，运行：

```sh
$ coverage run manage.py test --settings=twoscoops.settings.test
```

可能会返回：

```
Creating test database for alias "default"...
..
-----------------------------------------------
Ran 2 tests in 0.008s
OK
Destroying test database for alias "default"...
```

通过这种方式，我们只对自己的代码进行测试。

## 生成报告！

coverage.py 还能生成 HTML 格式的报告。在 &lt;project_root&gt; 目录下，运行：

```sh
$ coverage html --omit="admin.py"
```

之后在当前目录下会生成一个新的目录 **htmlcov/**，可以在目录下打开 **index.html** 文件。点击里面的各模块列表，其中的红色部分是不好的。

## 测试覆盖的基本原则

当新增功能和修复问题后，假设之前的覆盖率是 65%，那么修改后如果测试覆盖率低于 65%，代码就不要合并进来，从而保证的测试的覆盖率。

测试覆盖率缓慢地提高是好的，说明项目的质量一直在改善，绝不可跳跃式的提高。


## 其它的测试库

Django 的默认测试库是 unittest，使用它时，要写的样板文件比较多。

下面的两个库所需的样板文件较少：

+ [pytest-django](https://pypi.python.org/pypi/pytest-django/)
+ [django-nose](https://pypi.python.org/pypi/django-nose)

这两个库分别是对 pytest 和 nose 库的封装。它们不仅能运行 unittest 式的测试用例，还能测试任何以 **test_** 开头的函数（类/目录/模志）等。下面是一个简单的例子：

```python
# test_models.py
from pytest import raises

from cones.models import Cone

def test_good_choice():
	assert Cone.objects.filter(type='sugar').count() == 1

def test_bad_cone_choice():
	with raises(Cone.DoesNotExist):
		Cone.objects.get(type='spaghetti')
```


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
