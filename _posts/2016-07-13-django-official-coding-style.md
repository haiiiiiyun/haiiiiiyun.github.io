---
title: Django 官方代码风格指南学习摘要
date: 2016-07-13
writing-time: 2016-07-13 12:52--13:58
categories: programming
tags: python programming Django
---

# Python 风格

+ 以下没有特别提到的，都遵循 Python 的 [PEP8](http://www.python.org/dev/peps/pep-0008/) 约定，见[Python 代码风格指南 PEP8 摘要](/python-code-style-guide-pep8/)。

PEP 8 中限制行长最多 79 个字符，但 Django 允许最多到 119 个字符（这是 GitHub 代码审查工具允许的宽度）。 PEP 8 限制文档、注释、docstring 的行长为 72 个字符， Django 将它们限制到 79 个字符。

使用 [Flake8](https://flake8.readthedocs.io/en/latest/) 来检查代码质量。

+ 每层缩进使用 4 个空格

+ 变量、函数、方法名中使用下划线 `_`，而非 **camelCase** ，如应写成 `poll.get_unique_voters()`，而不要写成 `poll.getUniqueVoters()`

+ 类名和返回类的工厂函数名要用 **InitiaCaps** 形式

+ 尽可能使用便捷式的 `import`，比如使用 `from django.views.generic import View`，而不要用 `from django.views.generic.base import View`

+ 在 docstring 中，使用 "动作语句”，比如：

```
# 这样使用：
def foo():
    """
    Calculates something and returns the result.
    """
    pass
```

```
# 不要这样使用：
def foo():
    """
    Calculate something and return the result.
    """
    pass
```

# 模板风格

+ 标签内容两侧有且仅有一个空格，如 `{{ foo }}`，而不要 `{{foo}}`

# 视图风格

+ 视图函数的第一个参数应该为 `request`，如 `def my_view(request, foo):`，而不要用 `def my_view(req, foo):`

# 数据模型风格

+ 数据项名应该全部小写，使用下划线而不是 **camelCase**，如：

```
# 正确的风格：
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
```

```
# 错误的风格：
class Person(models.Model):
    FirstName = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=40)
```

+ `class Meta` 应该放置在数据项定义之后，之间用一行空行分隔，如：

```
# 正确的风格：
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'people'
```

```
# 不要这样写：
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = 'people'
```

```
# 也不要这样写
class Person(models.Model):
    class Meta:
        verbose_name_plural = 'people'

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
```

+ 如果定义了 `__str__`（支持 Python 3 前是 `__unicode__`），应在数据模型的 class 上使用 `python_2_unicode_compatible()` 修饰器。

+ 数据模型 class 内的布局顺序：
    1. 数据项定义
    2. 定制的 manager 
    3. `class Meta`
    4. `def __str__()`
    5. `def save()`
    6. `def get_absolute_url()`
    7. 其它定制的方法

+ `choices` 应定义为元组的元组，单字符的选项名应该设置为类中的属性，因为是常量、使用全大写风格，如：

```
class MyModel(models.Model):
    DIRECTION_UP = 'U'
    DIRECTION_DOWN = 'D'
    DIRECTION_CHOICES = (
        (DIRECTION_UP, 'Up'),
        (DIRECTION_DOWN, 'Down'),
    )
```

# django.conf.settings 的使用

在模块顶层（当模块被 import 时会自动执行的部分）不要存取 `django.conf.settings`。 Django 项目只能调用 `django.conf.settings.configure()` 函数一次（仅一次）来对 settings 进行配置。settings 是一个 `LazyObject` 对象，对其存取时才会真正调用 `django.config.settings.configure()` 来对 settings 进行配置。

如果在模块顶层对其进行了存取，就会自动完成对 `django.conf.settings.configure()` 的调用，从而会影响之后的 settings 的配置。

#  其它

+ 所有字符串都应进行国际化标记
+ 随着代码的演进，去除不用了的 `import`，flake8 会对没用到的 `import` 显示警告信息，如果想去除，在代码行尾加 `# NOQA`
+ 去除行尾多余的空白符
+ 不要将贡献者的名字写在代码中，应写在一个独立的 `AUTHORS` 文件中

> 参考文献： [Django Coding style](https://docs.djangoproject.com/en/1.8/internals/contributing/writing-code/coding-style/)
