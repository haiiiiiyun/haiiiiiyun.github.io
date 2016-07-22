---
title: Django 的查询和数据库层
date: 2016-07-22
writing-time: 2016-07-22 16:10
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 对应获取单个对象应使用 get_object_or_404()

在视图代码中，要获取单个对象，不要用 get(), 而是用 get_object_or_404()。

get_object_or_404() 会返回 404 页。因此只能用于视图中。

# 小心处理可以抛出异常的查询操作

## ObjectDoesNotExist vs. DoesNotExist

ObjectDoesNotExist 能应用于所有的数据模型对象，而 DoesNotExist 只适用于某个特定的数据模型。

例如：

```
from django.core.exceptions import ObjectDoesNotExist

from flavors.models import Flavor
from store.exceptions import OutOfStock

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)

def list_any_line_item(model, sku):
    try:
        return model.objects.get(sku=sku, quantity__gt=0)
    except ObjectDoesNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)
```

## 当想获取单个对象却返回了多个时

应该对 MultipleObjectsReturned 异常进行处理，如：

```
from flavors.models import Flavor
from store.exceptions import OutOfStock, CorruptedDatabase

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are out of {}".format(sku)
        raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = "Multiple items have SKU {}. Please fix!".format(sku)
        raise CorruptedDatabase(msg)
```

## 利用惰性求值特性使查询语句更清晰

Django ORM 的惰性求值特性：只在确实需要数据时才进行 SQL 操作。因此可以将串连起来的 ORM 方法和函数拆分到多行上，不必放在同一行。

因此，不要这样写：
```
from django.models import Q

from promos.models import Promo

def fun_function(**kwargs):
    # Too much query chaining makes code go off the screen or page. Not good.
    return Promo.objects.active().filter( Q(name__startswith=name) | Q(description__icontains=name)).exclude(status='melted').select_related('flavors')
```

而应该这样写：

```
from django.models import Q

from promos.models import Promo

def fun_function(**kwargs):
    """Find working ice cream promo"""
    results = Promo.objects.active()
    results = results.filter(
            Q(name__startswith=name) |
            Q(description__icontains=name)
        )
    results = results.exclude(status='melted')
    results = results.select_related('flavors')
    return results
```

# 使用高级查询工具

相同的数据处理任务，直接在数据库中完成总是比先获取数据，再用 Python 处理快的多。使用高级查询工具，使工作直接在数据库中完成，不仅能提高性能，而且能提高代码的可靠性。

## 查询表达式

对于下面的代码：

```
from models.customers import Customer

customers = []
for customer in Customer.objects.iterate():
    if customer.scoops_ordered > customer.store_visits:
        customers.append(customer)
```

有几个问题：

+ 使用循环速度较慢、内存使用较高
+ 循环过程中，数据有可以被更新了，从而使处理的数据不精确


因此，应该用下面这种更高效的方法：

```
from django.db.models import F

from models.customers import Customer

customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
```

它相当于执行如下 SQL 语句：

```
SELECT * from customers_customer where . scoops_ordered > store_visits
```

## 数据库函数

在 Django 1.8 中我们可以调用数据库提供的通用函数如 UPPER()、LOWER()、COALESCE()、CONCAT()、LENGTH() 和 SUBSTR()。

推荐使用这些函数：

+ 它们非常方便使用
+ 通常数据库函数可以将一些逻辑从 Python 移到数据库中。这有利于提高性能
+ Django ORM 将数据库函数进行了抽象，因此相同的函数可以应用于所有支持的数据库中
+ 它们也是查询语句，因此也遵循 ORM 的通用模式

# 非必要时不要使用原始 SQL

ORM 非常适合于普通的使用情况，同时提供模型访问/更新功能以及完整的验证和安全功能。因此尽量使用 ORM。

SQL 会特定于某个数据库，因此会降低可移植性。

当需要将数据从一种数据库迁移到另一种数据库时，你的 SQL 语句中使用的只针对特定数据库的功能会出现问题。

那么何时使用原始 SQL？

+ 当它能显著简化你的 Python 代码或者 ORM 生成的 SQL 代码时。







> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
