---
title: 推荐的 Django 代码风格
date: 2016-07-13
writing-time: 2016-07-13 08:27--12:50
categories: programming
tags: python Django programming
---

# 目标

* 变量名避免使用缩写词
* 函数参数名要有意义
* 类和方法一定要有文档
* 写好注释
* DRY，将重复的代码行重构成函数或方法
* 函数和方法所含的代码行要保持短小。一个很好的检验法则是：无需滚动就可以看到整个的函数/方法体。

# PEP 8

遵循 Python 的 [PEP8](http://www.python.org/dev/peps/pep-0008/) 约定，见[Python 代码风格指南 PEP8 摘要](/python-code-style-guide-pep8/)。

1. 每层缩进使用 4 个空格
2. 开源项目每行限制最长 79 个字符，私人项目每行可限制为 99 个字符
3. 顶层函数和类的定义要用两行空行分隔
4. 类中的方法定义用一行空行分隔
5. `import` 顺序：
    1): 标准库
    2): Django 核心代码库
    2): 与 Django 相关的第三方代码库
    3): 自己项目的代码库

    例如：

```
# Stdlib imports
from __future__ import absolute_import
from math import sqrt
from os.path import abspath

# Core Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Third-party app imports
from django_extensions.db.models import TimeStampedModel

# Imports from your apps
from splits.models import BananaSplit
```

6. 使用显式的相对导入法，如：

```
from __future__ import absolute_import
from django.views.generic import CreateView

# Relative imports of the 'cones' package
from .models import WaffleCone
from .forms import WaffleConeForm
from core.views import FoodMixin
```

7. 不要使用 `import *`，它会污染你的代码命名空间。

举例来说， `django.forms` 中有 `CharField`，`django.db.models` 也有 `CharField`， 那么以下的代码：

```
from django.forms import *
from Django.db.models import *
```

导入的 models 中的 `CharField` 将覆盖 forms 中的 `CharField`。

# Django 代码风格指南

1. Django 项目优先遵循 [Django 自己的风格](https://docs.djangoproject.com/en/1.8/internals/contributing/writing-code/coding-style/)。

2. 在 URL Pattern 中使用下划线 `_`，不要用破折号 `-`，如：

```
patterns = [
    url(regex='^add/$',
        view=views.add_topping,
        name='add_topping'),
]
```

3. 在 模板 block 名中使用下划线 `_`，不要用破折号 `-`

# JS、HTML 与 CSS 风格指南

## JavaScript 代码风格

JavaScript 没有官方的风格指南，推荐以下几种风格，可以选一种适合自己口味的。

+ [idiomatic.js: 编写一致、地道的 JavaScript 代码](https://github.com/rwaldron/idiomatic.js/)
+ [Pragmatic.js 代码风格指南](https://github.com/madrobby/pragmatic.js)
+ [Airbnb JavaScript 风格指南](https://github.com/airbnb/javascript)
+ [Node.js 风格指南](https://github.com/felixge/node-style-guide)
+ [JavaScript 编程语言代码规范](http://javascript.crockford.com/code.html)

可以使用 [JSCS]( http://jscs.info/ ) 工具来对 JavaScript 代码风格进行检查。


## HTML 和 CSS 风格指南

+ 由 [@mdo](https://twitter.com/mdo) 编写的 [HTML 和 CSS 代码指南](http://codeguide.co)
+ [idomatic-css: 编写一致、地道的 CSS](https://github.com/necolas/idiomatic-css)

可以使用 [CSScomb]( http://csscomb.com/ ) 工具来对 CSS 代码风格进行检查。

# 千万不要将你的项目布局绑死到某个特定的 IDE（或编辑器）

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
