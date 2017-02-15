---
title: Django REST 框架 V3 教程 1 - 序列化功能
date: 2017-02-15
writing-time: 2017-02-15 11:41--16:41
categories: Programming
tags: Programming djangorestframework Django Python REST
---

# 概述

本系列教程中创建的项目实现了有关代码高亮的 一组 Web API。

开发环境和项目初始化见 [Django REST 框架 V3 Quickstart](http://www.atjiang.com/django-rest-quickstart/) 中的内容。

# Snippets 示例项目

## 项目依赖

代码高亮功能依赖包 pygments，可以用 pip 安装：

```bash
$ pip install pygments
```

## 项目创建

在 tutorial 项目中创建 snippets 应用：


```bash
$ cd django-rest-framework-v3/tutorial/tutorial

$ django-admin.py startapp snippets
$ cd ..
```

在 `tutorial/settings.py` 中配置 INSTALLED_APPS:

```python
INSTALLED_APPS = (
    # ...,
    'rest_framework',
    'tutorial.snippets.apps.SnippetsConfig',
)
```

在 `tutorial/snippets/apps.py` 中，将 `name = 'snippets'` 改为 `name = 'tutorial.snippets'`。

若使用 Django &lt; 1.9, 需要将上面的 `tutorial.snippets.apps.SnippetsConfig` 替换成 `tutorial.snippets`。

## Model

创建 Model Snippet 用来保存代码段数据：

```python
# file: tutorial/snippets/models.py
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created', )
```

这里 `LANGUAGE_CHOICES` 提取出了 pygments 支持的所有计算机语言列表，而 `STYLE_CHOICES` 提取出了 pygments 支持的所有格式化风格列表。

同步数据库：

```bash
$ python manage.py makemigrations snippets
$ python manage.py migrate
```

## 创建 Serializer 类

提供对 snippet 实例进行序列化和反序列化支持是实现 Web API 的首要任务。要将 snippet 实例序列化成 `json` 等格式表示，需要定义 snippet 的 Serializer 类，这和定义 snippet 的 Django Form 类非常类似。

```python
# file: tutorial/snippets/serializers.py
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated_data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated_data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```

该 Serializer 类定义了 Snippet 中需要序列化/反序列化的各项。而其中的 `create()` 和 `update()` 函数会在 `Serializer.save()` 时相应调用。

Serializer 类非常类似 Django 的 Form 类，并且在项定义时也支持类似的参数，能 required, max_length, default 等。

`style={'base_template': 'textarea.html'}` 表示该 Serializer 项在浏览器上按 Textarea 方式显示，该参数等同于 Django Form 中的 `widget=widgets.Textarea`。

这个 Serializer 是基于 Snippet Model 定义的，我们也可以通过使用 `ModelSerializer` 简化上面的代码。

## 使用 Serializer

在 Django Shell 中测试使用：

```python
from tutorial.snippets.models import Snippet
from tutorial.snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo="bar"\n')
snippet.save()

snippet = Snippet(code='print "Hello, world"\n')
snippet.save()

serializer = SnippetSerializer(snippet)
serializer.data
#Out[13]:
ReturnDict([('id', 2),
            ('title', u''),
            ('code', u'print "hello, world"\n'),
            ('linenos', False),
            ('language', 'python'),
            ('style', 'friendly')])

# 序列化成 JSON 格式显示
content = JSONRenderer().render(serializer.data)
content
#Out[15]: '{"id":2,"title":"","code":"print \\"hello, world\\"\\n","linenos":false,"language":"python","style":"friendly"}'

# 反序列化也很简单，先将内容解析成 Python 中的类型：
from django.utils.six import BytesIO

stream = BytesIO(content)
data = JSONParser().parse(stream)

# 然后还原成对象实例
serializer = SnippetSerializer(data=data)
serializer.is_valid()
#Out[17]: True
serializer.validated_data
#Out[18]: 
OrderedDict([(u'title', u''),
             (u'code', u'print "hello, world"'),
             (u'linenos', False),
             (u'language', 'python'),
             (u'style', 'friendly')])
serializer.save()
#Out[19]: <Snippet: Snippet object>

# 除了可以序列化一个实例外，也可以对 querysets 进行序列化，只需加 many=True 即可。
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
#Out[21]: [OrderedDict([('id', 1), ('title', u''), ('code', u'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', u''), ('code', u'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', u''), ('code', u'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```

## 使用 ModelSerializer

类似 Django 提供了 Form 和 ModelForm，Serializer 也有对应的 ModelSerialzier。

通过使用 ModelSerializer，可以将 `snippets/serializers.py` 重构如下：

```python
# file: tutorial/snippets/serializers.py
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
```

在 Django Shell 中，通过 `print(repr(serializer)` 可以查看这个由 ModelSerializer 创建的 Serializer 内的具体项定义：

```python
from tutorial.snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))
# SnippetSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    title = CharField(allow_blank=True, max_length=100, required=False)
#    code = CharField(style={'base_template': 'textarea.html'})
#    linenos = BooleanField(required=False)
#    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
#    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
```

## 在普通的 Django View 中使用 Serializer

本例中暂时禁用了 Django 的 CSRF 功能。

```python
# file: tutorial/snippets/views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# A view that supports listing all the existing snippets, or creating a new snippet.
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new one.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

# A view that corresponds to an individual snippet, can be used to
# retrieve, update or delete the snippet.
@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
```

最后，定义 URL：

```python
# file: tutorial/snippets/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
```

```python
# file: tutorial/urls.py
from django.conf.urls import url, include

urlpatterns = [
    url(r'^snippets/', include('tutorial.snippets.urls')),
]
```

## 使用测试

使用 httpie 测试：

```bash
$ http http://127.0.0.1:8000/snippets/snippets/

HTTP/1.0 200 OK
Content-Type: application/json
Date: Wed, 15 Feb 2017 08:29:39 GMT
Server: WSGIServer/0.1 Python/2.7.12
X-Frame-Options: SAMEORIGIN

[
    {
        "code": "foo = \"bar\"\n", 
        "id": 1, 
        "language": "python", 
        "linenos": false, 
        "style": "friendly", 
        "title": ""
    }, 
    {
        "code": "print \"hello, world\"\n", 
        "id": 2, 
        "language": "python", 
        "linenos": false, 
        "style": "friendly", 
        "title": ""
    }, 
    {
        "code": "print \"hello, world\"", 
        "id": 3, 
        "language": "python", 
        "linenos": false, 
        "style": "friendly", 
        "title": ""
    }
]

$ http http://127.0.0.1:8000/snippets/snippets/2/

HTTP/1.0 200 OK
Content-Type: application/json
Date: Wed, 15 Feb 2017 08:30:23 GMT
Server: WSGIServer/0.1 Python/2.7.12
X-Frame-Options: SAMEORIGIN

{
    "code": "print \"hello, world\"\n", 
    "id": 2, 
    "language": "python", 
    "linenos": false, 
    "style": "friendly", 
    "title": ""
}
```

# 参考 

+ [Tutorial 1: Serialization](http://www.django-rest-framework.org/tutorial/1-serialization/)
