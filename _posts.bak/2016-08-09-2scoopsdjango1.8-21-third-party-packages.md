---
title: Django 的第三方包
date: 2016-08-09
writing-time: 2016-08-09 13:34--16:03
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

+ 第三方仓库 [Python Package Index(PyPI)](https://pypi.python.org/pypi)

+ [Django 第三方包信息库](https://www.djangopackages.com)

Django 项目中的 Requirements 文件中的依赖包一定要指定特定的版本号，如：

```conf
Django==1.8
coverage==3.7.1
django-extensions==1.5.2
django-braces==1.4
```

而你发布的第三方包中，依赖包不能指定特定的版本，版本号要越宽泛越好。例如，当你的依赖指定为 `Django==1.72`, 但当你的包在 Django 1.8 的项目中使用时，就会出现冲突。


有用的包资源：

## 核心
[Django](https://djangoproject.com) : Web 框架。

[django-debug-toolbar](http://django-debug-toolbar.readthedocs.org/) : 显示面板用于调试 Django HTML 视图。

[django-model-utils](https://pypi.python.org/pypi/django-model-utils) : 很有用的数据模型工具，包含一个时间戳数据模型。

[ipdb](https://pypi.python.org/pypi/ipdb) : IPython pdb。

[Pillow](https://pypi.python.org/pypi/Pillow) : PIL 替代品。

[pip](http://www.pip-installer.org) : 包安装工具。在 Python 3.4 及以上版本中已内置。

[Sphinx](http://sphinx-doc.org/) : Python 项目的文档工具。

[virtualenv](http://virtualenv.org) : Python 虚拟环境。

[virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/) : 使得 virtualenv 在 Mac OS X 和 Linux 上更加好用。

[virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win) : 使得 virtualenv 在 Windows 上更加好用。

## 异步

[celery](http://www.celeryproject.org/) : 分布式任务队列。

[flower](https://pypi.python.org/pypi/flower) : 监测和管理 Celery 任务的工具。

[rq](https://pypi.python.org/pypi/rq) : RQ 是一个简单轻量级的库，用于创建和处理后台任务。

[django-rq](https://pypi.python.org/pypi/django-rq) : 用于在 Django 中集成 RQ (Redis Queue) 的一个简单应用。

[django-background-tasks](https://pypi.python.org/pypi/django-background-tasks) : 数据库异步任务队列。

## 数据库

[django-db-tools](https://pypi.python.org/pypi/django-db-tools) : 对于将网站往返切换到只读模式很有用。

[psycopg2](https://pypi.python.org/pypi/psycopg2) : PostgreSQL 数据库适配器。

## 部署

[circus](https://pypi.python.org/pypi/circus) : 能使你运行和监测多进程和多 Socket 的一个程序。用于 Mozilla，非常复杂，不适合小项目。

[dj-database-url](https://pypi.python.org/pypi/dj-database-url) : 这个简单的 Django 工具能使你轻松地使用 Heroku 访问数据库。

[django-heroku-memcacheify](https://pypi.python.org/pypi/django-heroku-memcacheify) : 为 Heroku 提供简单的 Memcached 配置。

[Fabric](https://pypi.python.org/pypi/Fabric) : 用于远程执行和部署的简单工具。

[Invoke](https://pypi.python.org/pypi/invoke) : 类似 Fabric, 但它兼容 Python 3。

[Paver](https://pypi.python.org/pypi/invoke) : 一个创建、发布和部署的脚本工具。

[Supervisor](http://supervisord.org/) : Supervisord 是一个 C/S 系统，它用于监测和控制类 UNIX 系统上的鑫个进程。

## 表单

[django-crispy-forms](http://django-crispy-forms.readthedocs.org/) : 为 Django 表单呈现控件。默认使用 Twitter Bootstrap 组件，但是可替换。

[django-floppyforms](http://django-floppyforms.readthedocs.org/) : 表单项、组件和布局，可与 django-crispy-forms 一起使用。

[django-forms-bootstrap](https://pypi.python.org/pypi/django-forms-bootstrap) : 一个简单的表单过滤器，使用 Twitter Bootstrap 型的 Django 表单中。

[django-forms-builders](https://github.com/stephenmcd/django-forms-builder) : 一个可重用的 Django 应用，为管理员用户提供在 admin 界面中创建自定义表单的功能。


## 前端 
[JSCS](http://jscs.info/) : JavaScript 代码风格检查器。

[CSScomb](http://csscomb.com/) : CSS 代码风格格式化工具。

## 日志

[logutils](https://pypi.python.org/pypi/logutils) : 为 logging 提供了很有用的 handlers。

[Sentry](http://getsentry.com) : 开源的异常错误聚合器。

[App Enlight](https://appenlight.com/ ) : 跟踪项目中的项目和性能问题。

[Newrelic](http://newrelic.com) : 实时日志和聚合平台。

## 项目模板
[cookiecutter-django](https://github.com/pydanny/cookiecutter-django) 。

[Cookiecutter](http://cookiecutter.readthedocs.org) : 不只针对 Django。是一个用于创建项目和应用模板的命令行工具。它专注、测试充分、文档充实。

[django-kevin](https://github.com/imkevinxu/django-kevin) : 特别针对 Heroku 部署优化的 Django 项目模板。

[django-herokuapp](https://github.com/etianen/django-herokuapp) : 提供一组工具和项目模板，使 Django 网站易于在 Heroku 上运行。


## REST APIs

[django-rest-framework](http://django-rest-framework.org/) : Django REST 包的事实标准。能将数据模型和非数据模型资源导出为 RESTful API。

[django-jsonview](https://github.com/jsocol/django-jsonview) : 提供一个简单的装饰器，能将 Python 对象转成 JSON 并确保已装饰的视图总能返回 JSON。

[django-tastypie](http://django-tastypie.readthedocs.org) : 能将数据模型和非数据模型资源导出为 RESTful API。


## 安全
[bleach](https://pypi.python.org/pypi/bleachbleach) : 一个简单基于白名单的 HTML 安全审查工具。

[defusedxml](https://pypi.python.org/pypi/defusedxml) : 当需要从外部接收 XML 数据时必须要用的 Python 库。

[django-autoadmin](https://pypi.python.org/pypi/django-autoadmin) : 为 Django 项目的管理员用户自动生成密码。

[django-admin-honeypot](https://pypi.python.org/pypi/django-admin-honeypot) : 一个假的 Django 管理登录界面，用于通知管理员有关未授权访问的情况。

[django-axes](https://github.com/django-pci/django-axes) : 为 Django 站点记录失败的登录尝试。

[django-ratelimit-backend](https://pypi.python.org/pypi/django-ratelimit-backend) : 在 auth backend 层进行登录速率限定。

[django-passwords](https://pypi.python.org/pypi/django-passwords) : 一个可重用的 Django 应用，为验证密码强度提供了验证器和一个表单项。

[django-secure](https://pypi.python.org/pypi/django-secure) : 有助于你采用安全专家推荐的实践对站点进行安全加固。它的大部分功能已包含在 Django 的 SecurityMiddleware 类中。

[django-two-factor-auth](https://pypi.python.org/pypi/django-two-factor-auth) : 针对 Django 的完整双因子认证。

[django-user-sessions](https://pypi.python.org/pypi/django-user-sessions) : 含一个 user 的 Django 会话。

[peep](https://pypi.python.org/pypi/peep) : 只使用已验证的 TLS 来上传至 PYPI，能保护你的信息不被窃取。其它的一些功能也值得一看。

[Twine](https://pypi.python.org/pypi/twine) : 只使用已验证的 TLS 来上传至 PYPI，能保护你的信息不被窃取。其它的一些功能也值得一看。


## 测试

[coverage](http://coverage.readthedocs.org/) : 检查你的代码有多少已经测试过了。

[factory boy](https://pypi.python.org/pypi/factory_boy) : 一个能创建数据模型测试数据的包。

[model mommy](https://pypi.python.org/pypi/model_mommy) : 另一个创建数据模型测试数据的包。

[mock](https://pypi.python.org/pypi/mock) : 不只针对 Django, 它能使你将系统中的部分组件替换为 mock 对象。该项目将会内置到 Python 3.4 中。

[pytest](http://pytest.org/) : 一个成熟的全功能 Python 测试工具，在 Python 和 Django 项目中都很有用。

[pytest-django](http://pytest-django.readthedocs.org/) : pytest-django 是针对 py.test 的一个插件，它提供的一组工具对 Django 应用和项目的测试很有用。

[tox](http://tox.readthedocs.org/) : 一个通用的 virtualenv 管理和命令行测试工具，能在命令行中用一个命令针对多个 Python 版本对项目进行测试。

## 用户注册
[django-allauth](http://django-allauth.readthedocs.org/) : 通用的注册和认证功能。包括电子邮件、Twitter、 Facebook、 GitHub、 Google 等。

[python-social-auth](http://django-social-auth.readthedocs.org/) : 针对 Twitter、 Facebook、 GitHub、 Google 等进行社交认证和注册。


## 视图
[django-braces](http://django-braces.readthedocs.org) : 为 Django CBV 提供了大量的 Mixin。

[django-extra-views](http://django-extra-views.readthedocs.org/) : 提供大量的额外通用 CBV 以对 Django 进行补充。

[django-vanilla-views](http://django-vanilla-views.org/) : 通过简化继承链来简化 Django 的通用 CBV。

## 时间
[python-dateutil](https://pypi.python.org/pypi/python-dateutil) : 为 Python datetime 模块提供了强大的扩展功能。

[pytz](https://pypi.python.org/pypi/pytz/) : 将 Olson tz 数据库融入 Python。它允许精确及跨平台的时区计算。它还解决了夏令时的时间问题。

## 其它

[awesome-slugify](https://pypi.python.org/pypi/awesome-slugify) : 一个灵活的 slugify 函数。

[dj-stripe](https://pypi.python.org/pypi/dj-stripe) : 使 Django + Stripe 更加容易。

[django-compressor](http://django-compressor.readthedocs.org/) : 将链接和内连的 JavaScript 和 CSS 压缩成单个的缓存文件。

[django-extensions](http://django-extensions.readthedocs.org/) : 提供 **shell plus** 管理命令及其它许多工具。

[django-haystack](http://django-haystack.readthedocs.org/) : 能与 SOLR、 Elasticsearch 等一起使用的全文检索工具。

[django-pipeline](http://django-pipeline.readthedocs.org/) : CSS 和 JS 的压缩工具，和 cssmin 与 jsmin 包一起使用。

[django-htmlmin](https://pypi.python.org/pypi/django-htmlmin) : Django 的 HTML minifier。

[django-reversion](https://pypi.python.org/pypi/django-reversion) : Django 框架的一个扩展，提供了完整的版本控制功能。

[django-watson](https://github.com/etianen/django-watson) : 为使用 SQL 数据库的 Django 项目提供全文多表的探索功能的应用。

[envdir](http://envdir.readthedocs.org/) : Python 版的 aemontools envdir。

[flake8](https://pypi.python.org/pypi/flake8) : 使用 PyFlakes, pep8 等其它工具进行代码质量检查。

[pathlib](https://pypi.python.org/pypi/pathlib ) : 面向对象的文件系统路径工具，已合并到 Python 3.4。

[pip-tools](https://github.com/nvie/pip-tools) : 一些能使你的 Python 依赖保持更新的工具。

[pyyaml](https://pypi.python.org/pypi/PyYAML) : Python 的 YAML 解析器和触发器。

[requests](http://docs.python-requests.org) : 一个易用的 HTTP 库，用于替换 Python 的 urllib2 库。

[silk](https://github.com/mtford90/silk) : Silk 是一个针对 Django 框架的 实时性能分析和检查工具。它在将数据呈现给用户界面之前将 HTTP 请求和数据库查询进行拦截，以便进一步进行分析。

[unicode-slugify](https://github.com/mozilla/unicode-slugify) : Mozilla 支持的一个 slugify，能使用 unicode 字符。

[Unipath](https://pypi.python.org/pypi/Unipath) : os/os.path/shutil 的面向对象的替代器。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
