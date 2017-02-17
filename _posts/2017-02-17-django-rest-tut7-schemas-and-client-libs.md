---
title: Django REST 框架 V3 教程 7 - Schema 和客户端库
date: 2017-02-17
writing-time: 2017-02-17 10:47--12:39
categories: Programming
tags: Programming djangorestframework Django Python REST coreapi
---

一个 schema 就是一个机器可读的文档，它对可用的 API 端点进行描述，给出它们的 URL，以及支持的操作。

服务端可以生成 schema 文档，而客户端可以基于该 schema 文档，与服务端交互。

# Core API

REST 框架通过 [Core API](http://www.coreapi.org/) 提供 schema 支持。

Core API 是一种用于描述 API 的文档标准。在服务端，通过 Core API 可以将 API 呈现成各种支持的 schema 或超媒体格式文件。而在客户端，在获取服务端生成的 schema 文件后，可以与服务端进行交互。

# 为服务端提供 schema 支持

REST 框架即支持手动定义 schema 视图，也支持自动生成 schema。因我们使用了 ViewSet 和 Router，故采用自动生成 schema 方式。

先安装依赖包 coreapi:

```bash
$ pip install coreapi
```

使用自动生成的 schema 视图定义 URL：

```python
#file: tutorial/snippets/urls.py
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    url(r'^schema/$', schema_view),
    #...
]
```

现在访问 URL http://127.0.0.1:8000/snippets/schema/ 将可以看到 `corejson` 的显示选项：

![corejson 显示选项](http://www.django-rest-framework.org/img/corejson-format.png)


也可以通过 httpie 工具进行访问，并通过 `Accept` 头指定返回 corejson 格式：

```bash
$ http http://127.0.0.1:8000/snippets/schema/ Accept:application/corejson+json
HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/coreapi+json

{
    "_meta": {
        "title": "Pastebin API"
    },
    "_type": "document",
    ...
```

默认的输出是 [Core JSON](http://www.coreapi.org/specification/encoding/#core-json-encoding)，其它支持的 schema 格式还有 [Open API](https://openapis.org/) 等。

# 客户端交互

服务端已经将 API 导出为 schema 文档了。客户端可以据此与服务端进行交互。

## 用 coreapi-cli 客户端命令行交互

先安装客户端命令行：

```bash
$ pip install coreapi-cli

$ coreapi
Usage: coreapi [OPTIONS] COMMAND [ARGS]...

  Command line client for interacting with CoreAPI services.

  Visit http://www.coreapi.org for more information.

Options:
  --version  Display the package version number.
  --help     Show this message and exit.

Commands:
  action       Interact with
  ...
```

测试使用：

```bash
$ coreapi get http://127.0.0.1:8000/snippets/schema/ # 加载 schema 文档
<Pastebin API "http://127.0.0.1:8000/snippets/schema/">
    snippets: {
        snippets: {
            list([limit], [offset])
            read(id)
            highlight(id)
        }
        users: {
            list([limit], [offset])
            read(id)
        }
    }

# 由于没有提供认证信息，现只能看到只读操作的 API
$ coreapi action snippets snippets list # 列出所有的 Snippet

{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://127.0.0.1:8000/snippets/snippets/1/",
            "id": 1,
            "highlight": "http://127.0.0.1:8000/snippets/snippets/1/highlight/"$
            "owner": "admin",
            "title": "",
            "code": "foo = \"bar\"\n",
            "linenos": false,
            "language": "python",
            "style": "friendly"
        },
        // ...
}

# 有些 API 需要传一个命名参数，例如:

$ coreapi action snippets snippets highlight --param id=1

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
  <title>Example</title>
  ...
```

## 认证客户端

客户端需要认证后，才能进行创建、编辑、删除等操作。

```bash
# 基于 basic auth 添加认证信息进行认证
$ coreapi credentials add 127.0.0.1 your_username:your_password --auth basic
Added credentials
127.0.0.1 "Basic ..."

# 现重新加载 schema 后，可看到所有的 API，包括创建，删除等 API
$ coreapi reload

<Pastebin API "http://127.0.0.1:8000/snippets/schema/">
    snippets: {
        snippets: {
            list([limit], [offset])
            create(code, [title], [linenos], [language], [style])
            read(id)
            update(id, code, [title], [linenos], [language], [style])
            partial_update(id, [title], [code], [linenos], [language], [style])
            delete(id)
            highlight(id)
        }
        users: {
            list([limit], [offset])
            read(id)
        }
    }

# 创建一个 snippet
$ coreapi action snippets snippets create --param title="Example" --param code="print('hello, world')"
{
    "url": "http://127.0.0.1:8000/snippets/snippets/7/",
    "id": 7,
    "highlight": "http://127.0.0.1:8000/snippets/snippets/7/highlight/",
    "owner": "admin",
    "title": "Example",
    "code": "print('hello, world')",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}

# 删除一个 snippet
$ coreapi action snippets snippets delete --param id=7
```

## 客户端库交互

客户端命令行可以进行的交互也都可以通过客户端库进行，例如 [Python 库](https://github.com/core-api/python-client) 和 [Javascript 库](https://github.com/core-api/javascript-client)。



# 参考 

+ [Tutorial 7: Schemas &amp; client libraries](http://www.django-rest-framework.org/tutorial/7-schemas-and-client-libraries/)
