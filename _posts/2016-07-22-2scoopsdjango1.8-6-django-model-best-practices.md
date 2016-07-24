---
title: Two Scoops Django 推荐的数据模型最佳实践
date: 2016-07-22
writing-time: 2016-07-21 08:29--2016-07-22 16:02
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

添加或修改数据模型都不能马虎，有关数据的操作都需慎重考虑。


推荐使用的 Django 数据模型相关的包：

1. **django-model-utils**: 使用其 TimeStampedModel
1. **django-extensions**: 使用其管理命令 **shell_plus**，它会自动加载所有已安装应用的数据模型


# 基础

## 将具有很多数据模型的应用进行拆分

推荐每个应用的数据模型数不超过 5 个。如果一个应用的数据模型数太多，意味着该应用做的事太多了，需要进行拆分。

## 慎重选择数据模型继承方式

Django 支持三种继承方式：

1. 抽象基类
2. 多表继承
3. 代理模型

**Django 抽象基类和 Python 的抽象基类是不同的！，它们有不同的目的和行为。**

各种继承方式的优缺点：

继承方式                                                                            | 优点                                                                                                   | 缺点
------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
抽象基类：只有继承的子数据模型才会创建数据表                                        | 能在抽象父类中定义共同项来减少重复输入，同时没有多表继承的额外数据表和 join 操作的开销                   | 父类不能单独使用
多表继承：父类和子类都会创建对应的数据表。两者之间隐含有一个 **OneToOneField** 关联 | 因每个数据模型都有表，故可对父子各自进行查询操作。同时可以通过 **parent.child** 从父对象直接访问子对象 | 对子表的查询都会有一个与其所有父表的 join 操作。**非常不推荐使用多表继承!**
代理模型：只为原始数据模型创建数据表                                                  | 可以为原始数据模型创建一个别名，并添加不同的 Python 行为                                                 | 无法修改数据模型项


如何确定应该使用哪种继承方式：

+ 如果重叠量很少（只有一两个项），则不需要用继承，只需在两个数据模型中都进行定义
+ 如果两者间有较多的重复项，则应重构代码，将相同项放置到一个抽象基类中
+ 代理模型有时会很有用，但它与其它两种模型继承方式非常不同
+ 应避免使用多表继承，因其即增加了复杂度又提高了性能开销。可以用 **OneToOneField** 及 **ForeignKeys** 来代替。

## 数据模型继承实践： TimeStampedModel

在数据模型中增加 **created** 和 **modified** 两个时间戳项是个普遍的需求。可以写一个 TimeStampedModel 基类如下：

```
# core/models.py
from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

然后所有继承自该抽象基类的数据模型都会有这两项：

```
# flavors/models.py
from django.db import models
from core.models import TimeStampedModel

class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)
```

## 数据库 Migration

Django 内置一个强大的数据库修改传导库叫 **migrations**，即 **django.db.migrations**。

创建 migrations 的建议：

+ 一旦新建了一个应用或数据模型后，应立即为该新的数据模型创建初始的 django.db.migrations。其实我们只需用 **python manage.py makemigrations** 命令就能完成
+ 在运行之前要对生成的 migration 代码进行检查，特别当涉及到复杂修改的时候。同时使用 **sqlmigrate** 命令来核查实际使用的 SQL 语句
+ 使用 **MIGRATION_MODULES** 配置项来管理第三方应用的 migration
+ 不要在意生成的 migrations 很多，我们可以用 **squashmigrations** 命令对其进行合并


部署及管理 migrations:

+ 在部署前，应先检查能否对该 migrations 进行回滚。
+ 如果表中有数百万条数据，应在 staging 服务器上对该数量级的数据进行测试。在真实数据库上进行 migrations 花费的时间可能比预期的要多得多！
+ 如果使用 MySQL：
    * 在涉及模式修改前必须进行备份。MySQL 对模式修改不提供事务支持，因此不可能进行回滚
    * 如果可能，在执行修改前应将项目置于 *只读* 模式
    * 对涉及大量数量的表格进行模式修改会花费很多时间。不是几秒，也不是几分钟，而是用小时计算的！


# Django 数据模型设计

## 对数据库进行规范化

一个数据模型不应该包含有已在其它数据模型中保存过了的数据。

相关资源：

+ [http://en.wikipedia.org/wiki/Database_normalization](http://en.wikipedia.org/wiki/Database_normalization)

+ [http://en.wikibooks.org/wiki/Relational_Database_Design/Normalization](http://en.wikibooks.org/wiki/Relational_Database_Design/Normalization)

## 缓存应在逆规范化前进行

## 只有在绝对必要时才进行逆规范化

##  何时使用 Null 和 Blank

数据项类型                                                                         | 设置 null=True                                                                            | 设置 blank=True
-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
CharField, TextField, SlugField, EmailField, CommaSeparatedIntegerField, UUIDField | 不要这样设置。Django 的传统是将空值保存为空字符串，而获取的 NULL 或空值解析为空字符串     | 可以设置。如果你允许其对应的表单项接受空值。
FileField, ImageField                                                              | 不要这样设置。Django 只是将从 **MEDIA_ROOT** 到该文件的路径保存在 CharField, 因此规则同上 | 可以这样设置，规则如 CharField
BooleanField                                                                       | 不要这样设置。不要用这个 Field, 用 NullBoolField                                          | 不要这样设置
IntegerField, FloatField, DecimalField, DurationField 等                           | 如果你允许在数据库中存储 NULL 的话，可以这样设置                                          | 如果你允许其相应的表单组件接受空值，可以这样设置，同时要设置 null=True
DateFieldField, DateField, TimeField 等                                            | 如果你允许在数据库中存储 NULL 的话，可以这样设置                                          | 如果你允许其对应的表单组件接受空值，或者使用了 **auto_now**、**auto_now_add** 的话，可以这样设置。同时要设置 null=True
ForeignKey, ManyToManyField, OneToOneField                                         | 可以这样设置                                                                              | 可以这样设置
GenericIPAddressField                                                              | 可以这样设置                                                                              | 可以这样设置
IPAddressField                                                                     | 不推荐使用该项类型，已在 Django 1.7 中过时                                                | 不推荐使用该项类型


## 何时使用 BinaryField

该类型在 Django 1.8 中添加，用于存放原始二进制数据，或 **bytes**。在该类型项上无法进行 filter、exclude 或其它的 SQL 操作。但它在以下情况下有用：

+ MessagePack 格式的内容
+ 传感器原始数据
+ 压缩的数据。如 Sentry 保存为 BLOB 的数据， 但是由于历史原因需要进行 base64 编码

二进制数据串可以会很大，这将会拖慢数据库。此时应将内容保存在一个文件中，然后用 FileField 来引用。


**绝对不要通过 BinaryField 提供文件服务** ：

+ 对数据库的读写比对文件系统更慢
+ 你的数据库会变得越来越大，从而性能越来越低
+ 此时访问文件需要经过 Django 应用层和数据库层共两层。

## 尽量避免使用通用关联 models.field.GenericForeignKey

使用 GenericForeignKey 会使该外键不受完整性约束，有以下的问题：

+ 因在模型间缺少索引，从而会降低查询速度
+ 数据表可能会引用一条不存在的记录，数据有损坏的风险

其优势是：由于没有完整性约束，一个数据项可以关联到不同类型的记录。大多应用于 voting、 tagging、ratings 中。

可以使用 **ForeignKey** 和 **ManyToMany** 来实现 **GenericForeignKey** 的功能，从而即保证了数据的完整性，又提升了性能。

因此，

+ 尽量避免使用通用关联和 **GenericForeignKey**
+ 如果需要通用关联的话，尝试是否可以通过调整数据模型设计或使用新的 PostgreSQL 项来解决
+ 如果非用不可，最好使用一个现成的第三方应用

## PostgreSQL 特定的项：何时使用 Null 和 Blank

数据项类型                                                 | 设置 null=True                      | 设置 blank=True
-----------------------------------------------------------|-------------------------------------|
ArrayField                                                 | 可以设置                            | 可以设置
HStoreField                                                | 可以设置                            | 可以设置
IntegerRangeField, BigIntegerRangeField 和 FloatRangeField | 可以设置。如果你想在数据库中存储 NULL | 可以设置。如果你允许其对应的表单组件接受空值。同时要设置 null=True
DatatimeRangeField 和 DateRangeField                       | 同上                                | 同上


# 数据模型的 **_meta** API

**_meta** 在 Django 1.8 前只在内部使用的。现成该接口已经公开了。

**_meta** 的用途：

+ 获取数据模型的项列表
+ 获取数据模型中特定项的类（或及继承链或者其它衍生信息）
+ 可以确保你获取这些信息所使用的方式在以后的 Django 版本中不会改变

使用举例：

+ 创建一个 Django 数据模型的自省工具
+ 创建自定义的 form 库
+ 创建一个与 admin 类似的工具来编辑或与 Django 数据模型中的数据交互
+ 创建可视化或分析库，如分析以 "foo" 开头的项的信息


# 数据模型管理器

数据模型管理器用于限制一个数据模型类所有可能的数据记录。Django 为每个数据模型类都提供一个默认的管理器。

我们可以自己定义数据模型管理器，如：

```
from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):

    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(pub_date__lte=timezone.now(), **kwargs)


class FlavorReview(models.Model):
    review = models.CharField(max_length=255)
    pub_date = models.DateTimeField()

    # add our custom model manager
    objects = PublishedManager()
```

此时，如果我们想先查出所有的评论数，然后再查出已发表的评论数，可以这样做：

```
>>> from reviews.models import FlavorReview
>>> FlavorReview.objects.count()
35
>>> FlavorReview.objects.published().count()
31
```

对于替换数据模型的默认管理器，要特别小心：

+ 首先，使用数据模型继承时，抽象基类的子类会接收其父类的数据模型管理器，但是使用多表继承方式的子类却不会
+ 其次，第一个应用于数据模型类的数据模型管理器会被当作默认的管理器。这和常规的 Python 模式差别很大，从而会使返回的查询结果与预想的不同

因此， 应该将 **objects = models.Manager()** 放在所有的自定义数据模型管理器之前。

# 理解胖数据模型

**fat models** 的概念是：不要将数据相关的代码分散在视图和模板中，应将这些逻辑封装在数据模型的方法、类方法、属性甚至管理器的方法中。这样，所有的视图和任务都可以重用这些代码。

这种方式的缺点：会使数据模型的代码量越来越多，从而难以维护和理解。

因此，当数据模型的代码量变得很大很复杂后，应该将相关重复的代码独立出来放在 *Model Behavior* 或 *Helper Functions* 中。

## 数据模型的 Behaviors，又名 Mixins

数据模型的 Behaviors 通过使用 Mixins 来奉行组合和封装的理念。

相关资源： [使用纵使来减少重复代码](http://blog.kevinastone.com/django-model-behaviors.html)

## 无状态的 Helper Functions

将这些逻辑放在工具函数集中，使其得以分隔开，从而使得测试更加容易。缺点是：因这些函数是无状态的，需要传递所有的参数。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
