---
title: Two Scoops Django 推荐的 Settings 和 Requirements 文件设置
date: 2016-07-20
writing-time: 2016-07-20 14:15--16:31
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 基本原则

Django 1.8 有约 140 个配置项可通过 settings 模块进行设置。settings 模块在每次启动 Django 服务时进行初始化，因此对 settings.py 文件修改后，都要重启 Django 服务器才能生效。

1. 所有 settings 文件都应进行版本控制，包括对配置项的修改日期/时间和注释信息进行版本控制

2. DRY，通过 `import base_settings` 进行继承，避免复制粘贴

3. 机密信息不要放在版本控制中

# 使用多个 settings 文件

```
settings/
    __init__.py
    base.py
    local.py
    staging.py
    test.py
    production.py
```

并且每个 settings 文件都对应有一个 requirements 文件

settings 文件名        | 目的
-----------------------|
local.py, dev.py       | 本地开发环境配置内容，如 `DEBUG=True`, 开启 django-debug-toolbar 等
staging.py             | 针对 Staging 阶段的配置内容
test.py                | 针对运行测试的配置内容
production.py, prod.py | 生产环境下的配置内容
ci.py                  | 针对持续集成服务器的配置内容


使用方法：

1. shell 中

```
python manage.py shell --settings=twoscoops.settings.local
```

2. 启动服务

```
python manage.py runserver --settings=twoscoops.settings.local
```

3. 设置 **DJANGO_SETTINGS_MODULE** 和 **PYTHONPATH** 环境变量。若使用了 **virtualenv**，可以在每个环境的激活脚本中设置 **DJANGO_SETTINGS_MODULE** 和 **PYTHONPATH**。



## 一个开发环境中的 settings 文件的例子：

```
# settings/local.py
from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "twoscoops",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

INSTALLED_APPS += ("debug_toolbar", )
```

上面的例子中有 `from .base import *`， 这是 `import *` 在 Django 中唯一被赞成使用的地方。因为我们想在 settings 文件中覆盖所有的命名空间。


## 针对开发环境也可以有多个 settings 文件

基本原则是每个 settings 文件都需要版本控制。可针对不同的开发者创建相应的 settings 文件，如：

```
# settings/dev_pydanny.py
from .dev import *

# Set short cache timeout
CACHE_TIMEOUT = 30
```

而创建后的所有 settings 文件会是：

```
settings/
    __init__.py
    base.py
    dev.py
    dev_audreyr.py
    dev_pydanny.py
    local.py
    staging.py
    test.py
    production.py
```

# 将配置信息从代码中分离出来

将 **SECRET_KEY**、**API KEY** 等信息存放在代码库中有以下问题：

1. 这些信息针对每次部署都要变动

2. **SECRET_KEY** 等值是配置值，不是代码

3. 存放在代码库中，有代码库访问权限的人都能看到

4. 多数 PaaS 不提供针对单台服务器的配置功能


解决方案是使用 **环境变量**。

使用环境变量来存放 **SECRET_KEY** 等信息的好处：

1. 由于这些敏感信息已保存它处，你会毫不犹豫地对每个文件进行版本控制

2. 针对每次部署，不再需要对这些配置信息进行修改

3. 多数 PaaS 平台推荐使用环境变量，并提供了相应的配置和管理工具

## 如何在本地进行环境变量设置

在 Linux/Mac 的 **bash** 中，通过将配置代码添加到 **.bashrc**、**.bash_profile** 或 **.profile** 等文件后面进行配置。若使用 **virtualenv**，也可以在 virtualenv 的 *bin/activate* 脚本中添加配置代码进行配置：

配置代码：

```
$ export SOME_SECRET_KEY=1c3-cr3am-15-yummy

$ export AUDREY_FREEZER_KEY=y34h-r1ght-d0nt-t0uch-my-1c3-cr34m
```

在 Win 上，可以在 **cmd.exe** 中通过 **setx** 命令进行配置，也可以在 virtualenv 的 *bin/activate.bat* 脚本中进行配置。

配置代码：

```
> set SOME_SECRET_KEY 1c3-cr3am-15-yummy
```

**PowerShell** 比 **cmd.exe** 更加强大，在 Vista 及以上版本中可用。使用 PowerShell 进行环境变量设置：

只针对当前用户：

```
[Environment]::SetEnvironmentVariable("SOME_SECRET_KEY",
                                     "1c3-cr3am-15-yummy", "User")
[Environment]::SetEnvironmentVariable("AUDREY_FREEZER_KEY",
                        "y34h-r1ght-d0nt-t0uch-my-1c3-cr34m", "User")
```

针对本机的全部用户：

```
[Environment]::SetEnvironmentVariable("SOME_SECRET_KEY",
                                "1c3-cr3am-15-yummy", "Machine")
[Environment]::SetEnvironmentVariable("AUDREY_FREEZER_KEY",
                        "y34h-r1ght-d0nt-t0uch-my-1c3-cr34m", "Machine")
```

## 生产环境中的环境变量配置举例

1. 在 Heroku 上配置

```
$ heroku config:set SOME_SECRET_KEY=1c3-cr3am-15-yummy
```
2. 在 Python 中存取这些配置信息

```
>>> import os
>>> os.environ["SOME_SECRET_KEY"]
"1c3-cr3am-15-yummy"
```

3. 在 settings 文件中存取这些配置信息

```
# Top of settings/production.py
import os
SOME_SECRET_KEY = os.environ["SOME_SECRET_KEY"]
```

## 对未设置 SECRET_KEY 的异常进行处理

如果没有 SECRET_KEY 值， 上面的存取代码会抛出 **KeyError**，项目也无法启动。但是该异常没有提供有效的提示信息，不利于调试。

在 *settings/base.py* 中使用以下代码进行处理：

```
# settings/base.py
import os

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)
```

然后在 settings 文件中，使用：

```
SOME_SECRET_KEY = get_env_variable("SOME_SECRET_KEY")
```

之后，如果没有设置 SOME_SECRET_KEY 这个环境变量，会出现以下的错误提示：

```
django.core.exceptions.ImproperlyConfigured: Set the SOME_SECRET_KEY
environment variable.
```

`manage.py` 会默认将 **DJANGO_SETTINGS_MODULE** 指向 **settings.py**，推荐在多 settings 文件时使用 `django-admin`，而单 settings 文件时使用 `manage.py`， 这两个命令基本是等同的：

```
$ django-admin <command> [options]
$ manage.py <command> [options]
```

# 当不能设置环境变量时

Apache 等使用自己的环境变量，如以上的针对系统的环境变量设置方法无效，此时可以将敏感信息保存在一个不可执行的文件中，并且不对该文件进行版本控制：

1. 为保存敏感信息生成一个文件，格式可以为 JSON、Config、YAML 或 XML。

2. 增加一个 loader 来对这些信息进行管理

3. 将该文件名增加到 *.gitignore* 和 *.hgignore*

## 使用 JSON 格式

1. 生成 secrets.json 文件：

```
{
    "FILENAME": "secrets.json",
    "SECRET_KEY": "I've got a secret!",
    "DATABASES_HOST": "127.0.0.1",
    "PORT": "5432"
}
```

2. 在 settings/base.py 中添加 loader，来存取这些信息：

```
# settings/base.py

import json

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# JSON-based secrets module
with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
```

#  使用多个 requirements 文件

每个 settings 文件需对应有一个 requirements 文件，并且对应不同的配置，只安装相应的依赖文件。

requirements 文件举例：

```
requirements/
    base.txt
    local.txt
    staging.txt
    production.txt
```

*base.txt* 中存放全局依赖，如：

```
Django==1.8.0
psycopg2==2.6
djangorestframework==3.1.1
```

而针对本地开发环境的 *local.txt*，可以在 *base.txt* 的基础上添加其它依赖：

```
-r base.txt # includes the base.txt requirements file

coverage==3.7.1
django-debug-toolbar==1.3.0
```

对于持续集成服务器的 *ci.txt* 可以是：

```
-r base.txt # includes the base.txt requirements file

coverage==3.7.1
django-jenkins==0.16.4
```

而 *production.txt* 基本会和 *base.txt* 相同，可能会是：

```
-r base.txt # includes the base.txt requirements file
```

## 安装

针对本地开发：

```
$ pip install -r requirements/local.txt
```

针对生产环境：

```
$ pip install -r requirements/production.txt
```

所有 requirements 文件中的依赖包都指定为特定的一个版本，这样能确保项目更加稳定。


# 在 settings 文件中处理文件路径

**不要对文件路径进行硬编码**

1. 使用 [Unipath](http://pypi.python.org/pypi/Unipath/) 进行文件路径处理

```
# At the top of settings/base.py
from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("static")
STATICFILES_DIRS = (
    BASE_DIR.child("assets"),
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIRS = (BASE_DIR.child("templates"),)
    },
]
```

2. 使用 **os.path** 进行文件路径处理

```
# At the top of settings/base.py
from os.path import join, abspath, dirname

here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)

# Configuring MEDIA_ROOT
MEDIA_ROOT = root("media")

# Configuring STATIC_ROOT
STATIC_ROOT = root("collected_static")

# Additional locations of static files
STATICFILES_DIRS = (
    root("assets"),
)

# Configuring TEMPLATE_DIRS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIRS = (root("templates"),)
    },
]
```


要找到你的配置文件与 Django 默认配置的区别，使用 Django 的 `diffsettings` 命令。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
