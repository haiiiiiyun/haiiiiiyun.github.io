---
title: Django 日志
date: 2016-08-16
writing-time: 2016-08-16 10:47--12:27
categories: programming
tags: Database Ubuntu Postgresql programming
---

日志能确保 Web 应用的稳定和健壮，它不仅能用于调试错误，而且能用于跟踪性能度量值。

记录异常活动并定期检查对服务器的安全也是至关重要的。

# 应用日志 VS 其它日志

应用日志是项目的 Python 代码产生的日志，其它的日志包括：服务器日志、数据库日志、网络日志等。各种日志都很重要。

# 何时使用各种不同级别的日志

在生产环境下，建议不使用 DEBUG 级的日志。

## 使用 CRITICAL 记录灾难性的日志

Django 源码中没有使用该种日志。

## 生产环境下的错误使用 ERROR 日志

Django 源码中的示例：

```python
# Taken directly from core Django code.
# Used here to illustrate an example only, so don't
# copy this into your project.
logger.error("Internal Server Error: %s", request.path,
    exc_info=exc_info,
    extra={
        "status_code": 500,
        "request": request
    }
)
```

当 **DEBUG=False** 时，每条 Error 日志会向 **ADMINS** 中设置的管理员发送邮件，内容包括：

+ 错误描述
+ 错误发生的 traceback
+ HTTP request

## 低危的问题用 WARNING

适用于异常或有潜在危险的问题。如 django-admin-honeypot 记录的登录尝试日志。

Django 在 CsrfViewMiddleware 中使用该日志，记录 **403 Forbidden** 错误。例如，当 POST 请求没有 csrf_token 时，记录如下：

```python
# Taken directly from core Django code.
# Used here to illustrate an example only, so don't
# copy this into your project.
logger.warning("Forbidden (%s): %s",
                REASON_NO_CSRF_COOKIE, request.path,
    extra={
        "status_code": 403,
        "request": request,
    }
)
```

## 有用的陈述性信息用 INFO

包括：

+ 关键组件的开启和关闭
+ 重要事件的状态修改
+ 权限更新，比如用户被授予了管理员权限

同时也可以用于性能分析中，用于查找性能瓶颈。

## 调试相关信息用 DEBUG

用于替换 print 语句。

不要这样记录日志：

```python
from django.views.generic import TemplateView

from .helpers import pint_counter

class PintView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super(PintView, self).get_context_data(**kwargs)
        pints_remaining = pint_counter()
        print("Only %d pints of ice cream left." % (pints_remaining))
        return context
```

而应该使用 logging 进行记录：

```python
import logging

from django.views.generic import TemplateView

from .helpers import pint_counter

logger = logging.getLogger(__name__)

class PintView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super(PintView, self).get_context_data(**kwargs)
        pints_remaining = pint_counter()
        logger.debug("Only %d pints of ice cream left." % pints_remaining)
        return context
```

在项目中到处使用 print 存在的问题：

+ 有可以会使站点崩溃
+ print 语句是无法记录的，一旦错过就不能回溯
+ print 语句不能在 Python 3 中使用

# 捕获异常后，记录 Traceback

Python 的 logging 模块支持：

+ Logger.exception() 自动包含 traceback 并且记录为 ERROR
+ 其它级别的日志，使用 exc_info 参数

下面是将 traceback 添加到 DEBUG 级日志的例子：

```python
import logging
import requests

logger = logging.getLogger(__name__)

def get_additional_data():
    try:
        r = requests.get("http://example.com/something-optional/")
    except requests.HTTPError as e:
        logger.exception(e)
        logger.debug("Could not get additional data", exc_info=True)
        return None
    return r
```

## 一个模块一个 Logger

```python
# You can place this snippet at the top
# of models.py, views.py, or any other
# file where you need to log.
import logging

logger = logging.getLogger(__name__)
```

# 在本地将日志记录到回滚文件

Django 默认将 ERROR 及以上的日志信息以邮件形式发送给 ADMINS 中的管理员，这是通过 Django 内置的 AdminEmailHandler 实现。

在本地，推荐将 INFO 及以上的日志记录到一个回滚文件中，在 UNIX 上创建回滚文件用 **logrotate** 工具，并使用 logging.handlers.WatchedFileHandler。

如果在 PAAS 上，也可以用 [Loggly](http://loggly.com) 服务实现。


# 其它建议

+ 调试时，使用 logger 的 DEBUG
+ 在 DEBUG 下运行测试后，再在 INFO 和 WARNING 级再次运行测试
+ 尽早增加日志功能
+ 当收到 ERROR 的邮件信息时，可以配置一个 [PagerDuty](http://www.pagerduty.com) 账号来对该项问题进行重复提醒，直到处理完毕。

有用的包：

**logutils** 包功能：

+ 对终端输出流进行着色
+ 将日志放入队列的功能
+ 提供为日志信息写单元测试的类
+ 一个增强的 HTTPHandler，可以支持 HTTPS

# 必读资料

+ https://docs.djangoproject.com/en/1.8/topics/logging/
+ http://docs.python.org/2/library/logging.html
+ http://docs.python.org/2/library/logging.config.html
+ http://docs.python.org/2/library/logging.handlers.html
+  http://docs.python.org/2/howto/logging-cookbook.html

# 有用的第三方工具

+ [Sentry](https://www.getsentry.com/) 能够收集错误日志。
+ [App Enlight](https://appenlight.com/) 能追踪应用中的错误和性能问题。
+ [loggly.com](http://loggly.com/) 简化了日志的管理，并提供有高效的查询工具。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
