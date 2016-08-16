---
title: Django Utilities
date: 2016-08-16
writing-time: 2016-08-16 21:58--23:28
categories: programming
tags: Database Ubuntu Postgresql programming
---

# 为工具类代码创建一个 core 应用

该应用通常命名为 core, common, generic, util 或 utils。

例如，假设项目中有一些自定义数据模型管理器和视图 Mixin 会在不同应用中使用，那么这个 core 应用会像这样：

```conf
core/
	__init__.py
	managers.py # contains the custom model manager(s)
	models.py
	views.py # Contains the custom view mixin(s)
```

同时，应该使这个 core 应用成为一个真正的 Django 应用。

当使用时，可以进行类似的 import :

```python
from core.managers import PublishedManager
from core.views import IceCreamMixin
```

# 使用 Utility 模块对应用进行优化

这些模块通常叫 *utils.py* 或 *helpers.py*。

## 在多处会用到的代码保存到 Utility 模块中

## 对数据模型瘦身

奉行 *fat model* 后，数据模型中的代码会越来越多，可以将其中的通用代码整理到 Utility 模块中。

## 更加易于测试

这些逻辑移到模块中的好处是更易于测试。在实现时，要注意这些工具类函数或类应该只关注一件事，并且将这件事做好。

# Django 自己的瑞士军刀

django.utils 包中有丰富的工具，但是这些工具大部分是内部使用的，因此不推荐在项目中使用。但是以下这些工具可以放心拿来使用。

## django.contrib.humanize

包含一系列的本地化模板过滤器，可以用于将用户数据转换成更加易于人类使用的格式。比如里面的 **intcomma** 过滤器可以将整数转化成包含逗号的字符串。

同时，这些过滤器也可以当作函数来使用。

## django.utils.decorators.method_decorator(decorator)

可以将我们的函数装饰器转变成类的方法装饰器

## django.utils.decorator_from_middleware(middleware)

Django 中间件本质上是全局的，可能会产生额外或隐式的查询操作。我们可以通过该装饰器将中间件只应用于某个视图上。

同时，也可以查看相关的 decorator_from_middleware_with_args 装饰器。

## django.utils.encoding.force_text(value)

将任何输入都转化成 Python3 中的 str 或 Python2 中的 unicode。

## django.utils.functional.cached_property

能将只有一个 self 参数的方法的返回值缓存到内存中，有效期是对象的生命周期。对性能优化非常有帮助，极力推荐使用。

使用方法见 [Django 文档](https://docs.djangoproject.com/en/1.8/ref/utils/#django.utils.functional.cached_property)。

该函数如果用在 Django 之外，在多线程环境下会有问题。因此可以看下第三方的 cached_property 库：

+ https://github.com/pydanny/cached-property
+ http://www.pydanny.com/cached-property.html

## django.utils.html.format_html(format_str, args, **kwargs)

和 Python 的 str.format() 方法类似，除了它是用于构造 HTML 段的。所有的 args 和 kwargs 在传给 str.format() 前都已转义。

使用方法见 [Django 文档](https://docs.djangoproject.com/en/1.8/ref/utils/#django.utils.html.format_html)。

## django.utils.html.strip_tags(value)

移除 HTML 标签并保留标签间的文本。需要注意的是，使用 strip_tags 后得到的内容，如果之前没有转义过，不能被认为是安全的。

## django.utils.six

## django.utils.text.slugify(value)

千万不要自己创建 slugify() 方法。django.templates.defaultfilters.slugify() 是它的别名。

默认的 slugify() 不支持非英语，如：

```python
>>> from django.utils.text import slugify
>>> slugify(u"straße") # German
u"strae"
```

但是，Mozilla 的 unicode-slugify 和 awesome-slugify 都支持 unicode，只是 unicode-slugify 会依赖 Django：

+ https://github.com/mozilla/unicode-slugify
+ https://github.com/dimka665/awesome-slugify

## django.utils.timezone

使用后，日期和时间在数据库中以 UTC 格式保存，并在需要时进行转换。

## django.utils.translate

# 异常

大多数异常都是内部使用的，但是有一些异常很实用。

## django.core.exceptions.ImproperlyConfigured

可在 settings 模块中导入使用。

## django.core.exceptions.ObjectDoesNotExist

它是所有 DoesNotExist 异常的基类。它在获取泛数据模型实例时很有用：

```python
# core/utils.py
from django.core.exceptions import ObjectDoesNotExist

class BorkedObject(object):
	loaded = False

def generic_load_tool(model, pk):
	try:
		instance = model.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return BorkedObject()
	instance.loaded = True
	return instance
```

通过使用该异常，还可以创建自己的 django.shortcuts.get_object_or_404 函数，甚至可以抛出 403 异常来代码 404 异常：

```python
# core/utils.py
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied

def get_object_or_403(model, **kwargs):
	try:
		return model.objects.get(**kwargs)
	except ObjectDoesNotExist:
		raise PermissionDenied
	except MultipleObjectsReturned:
		raise PermissionDenied
```

## django.core.exceptions.PermissionDenied

在视图中抛出该异常会返回 django.http.HttpResponseForbidden。

在安全需要高的项目中，可以通过该异常来向用户显示 “Permission Denied” 页：

```python
def finance_data_adjudication(store, sales, issues):

if store.something_not_right:
	msg = "Something is not right. Please contact the support team."
	raise PermissionDenied(msg)

# Continue on to perform other logic.
```

上面代码中，抛出该异常后，会显示 403 错误页。

说到 403 页，可以进行如下自定义：

```python
# urls.py

# This demonstrates the use of a custom . permission denied view. The default
# view is django.views.defaults.permission_denied
handler403 = 'core.views.permission_denied_view'
```

# 序列化和反序列化工具

Django 的序列化和反序列化工具支持对 JSON, Python, YAML 和 XML 等格式的处理。

下面是序列化的例子：

```python
# serializer_example.py
from django.core.serializers import get_serializer

from favorites.models import Favorite

# Get and instantiate the serializer class
# The 'json' can be replaced with 'python' or 'xml'.
# If you have pyyaml installed, you can replace it with
# 'pyyaml'
JSONSerializer = get_serializer("json")
serializer = JSONSerializer()

favs = Favorite.objects.filter()[:5]

# Serialize model data
serialized_data = serializer.serialize(favs)

# save the serialized data for use in the next example
with open("data.json", "w") as f:
	f.write(serialized_data)
```

下面是反序列化的例子：

```python
# deserializer_example.py
from django.core.serializers import get_serializer

from favorites.models import Favorite

favs = Favorite.objects.filter()[:5]

# Get and instantiate the serializer class
# The 'json' can be replaced with 'python' or 'xml'.
# If you have pyyaml installed, you can replace it with
# 'pyyaml'
JSONSerializer = get_serializer("json")
serializer = JSONSerializer()

# open the serialized data file
with open("data.txt") as f:
	serialized_data = f.read()

# deserialize model data into a generator object
# we'll call 'python data'
python_data = serializer.deserialize(serialized_data)

# iterate through the python_data
for element in python_data:
	# Prints 'django.core.serializers.base.DeserializedObject'
	print(type(element))

	# Elements have an 'object' that are literally instantiated
	# model instances (in this case, favorites.models.Favorite)
	print(
		element.object.pk,
		element.object.created
	)
```

对于上面的这两种使用情况，Django 已经提供了相关的工具： **dump-data** 和 **loaddata** 管理命令。

在使用 Django 内置的这些工具时，要时刻注意：它们会出错，它们对复杂数据结构支持不好。

因此：

+ 只对简单数据进行序列化
+ 数据库模式的修改会使序列化的数据失效
+ 不要只导入序列化数据。在存入数据库前使用 Django form 库对它们进行验证

## django.core.serializer.json.DjangoJSONEncoder

Python 内置的 JSON 模块对日期/时间或十进制数类型处理不太好，而 DjangoJSONEncoder 对这些支持的不错：

```python
# json_encoding_example.py
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

data = {"date": timezone.now()}

# If you don't add the DjangoJSONEncoder class then
# the json library will throw a TypeError.
json_data = json.dumps(data, cls=DjangoJSONEncoder)

print(json_data)
```

## django.core.serializers.pyyaml

相比于第三方库，它能对时间进行转换。

## django.core.serializers.xml_serializer

它整合了 Python 内置的 XML 处理器和 defusexml 库。


 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
