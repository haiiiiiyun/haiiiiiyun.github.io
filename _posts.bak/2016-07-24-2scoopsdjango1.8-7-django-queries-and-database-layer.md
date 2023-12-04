---
title: Django 的查询和数据库层
date: 2016-07-24
writing-time: 2016-07-22 16:10--2016-07-24 14:55
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 获取单个对象应使用 get_object_or_404()

在视图代码中，要获取单个对象，不要用 get(), 而是用 get_object_or_404()。

get_object_or_404() 会返回 404 页。因此只能用于视图中。

# 小心处理可能抛出异常的查询操作

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

相同的数据处理任务，直接在数据库中完成总比先获取数据，再用 Python 处理快的多。使用高级查询工具，使工作直接在数据库中完成，不仅能提高性能，而且能提高代码的可靠性。

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
SELECT * from customers_customer where scoops_ordered > store_visits
```

## 数据库函数

在 Django 1.8 中我们可以调用数据库提供的通用函数如 UPPER()、LOWER()、COALESCE()、CONCAT()、LENGTH() 和 SUBSTR()。

推荐使用这些函数：

+ 它们非常易用
+ 通常数据库函数可以将一些逻辑从 Python 移到数据库中。这有利于提高性能
+ Django ORM 将数据库函数进行了抽象，因此相同的函数可以应用于所有支持的数据库中
+ 它们也是查询语句，因此也遵循 ORM 的通用模式

# 非必要时不要使用原始 SQL

ORM 非常适合于普通的使用情况，同时提供模型访问/更新功能以及完整的验证和安全功能。因此尽量使用 ORM。

SQL 会特定于某个数据库，因此会降低可移植性。

当需要将数据从一种数据库迁移到另一种数据库时，你的 SQL 语句中使用的只针对特定数据库的功能会出现问题。

因此，只有当原始 SQL 能显著简化你的 Python 代码或者 ORM 生成的 SQL 代码才使用。


> Django 项目的联合领导者 Jacob Kaplan-Moss:
> 如果一个查询语句使用 SQL 语句比用 ORM 更方便，那就用 SQL 语句。
> extra() 很讨厌，应该避免使用; raw() 可以适当使用。


# 在必要时才添加索引

开始时不加索引，然后在必要时才在数据模型项中添加 **db_index=True**。

何时考虑添加索引：

+ 该索引被经常使用，比如在 10-25% 的查询中都能用到
+ 有真实数据，可以让我们分析索引的效果
+ 可以运行测试来检测索引是否提高了性能

如果使用 PostgreSQL， *pg_stat_activity* 可以告诉我们哪些索引有被使用。

# 事务

在 Django 1.8 中，ORM 的默认行为是对每个查询进行自动提交。当数据有修改时，比如每次的 *.create()* 和 *.update()* 操作，都会立即修改数据库中的数据。这种方式的优点是易于理解。缺点是：如果一个视图（或某些操作）中涉及两步或多步修改，当其中一步修改成功，而其它修改失败时，数据库有损坏的风险。

可以使用数据库事务来解决数据库损坏的风险。数据库事务能将两个或多个的数据库更新操作组装到一个单一的操作中。一旦某个更新操作失败，那么事务中的所有更新都将会被回滚。数据库事务，具有原子性、一致性、独立性和可持续性等特性（automic, consistent, isolated, durable)，即 ACID。


Django 1.8 对事务机制进行了重新修整，现在我们可以通过装饰器和上下文管理器更直观地锁定数据库的完整性。


## 将每次的 HTTP 请求都封装在一个事务中

```
# settings/base.py

DATABASES = {
    'default': {
        # ...
        'ATOMIC_REQUESTS': True,
    },
}
```

所有的请求都封装在一个事务中处理，包括那些只进行读操作的请求。这种方式的优点是安全性，缺点是可能影响性能。

如果项目有大量的写操作，这种方式能确保数据库的完整性。如果网站流量很大，我们再改用其它方式。

需要注意的是， ATOMIC_REQUESTS 只会回滚数据库的状态，如果在事务过程中调用了第三方接口，比如发送了邮件或短信，这些操作是不会回滚的。因此，如果有涉及这些操作，需要用 **transaction.non_atomic_requests()**。

可以先将整个视图设置为 non_atomic_requests，然后将视图中的某段代码设置在事务中，如：

```
# flavors/views.py
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Flavor

@transaction.non_atomic_requests
def posting_flavor_status(request, pk, status):
    flavor = get_object_or_404(Flavor, pk=pk)
    # This will execute in autocommit mode (Django's default).

    flavor.latest_status_change_attempt = timezone.now()
    flavor.save()

    with transaction.atomic():
        # This code executes inside a transaction.
        flavor.status = status
        flavor.latest_status_change_success = timezone.now()
        flavor.save()
        return HttpResponse("Hooray")

    # If the transaction fails, return the appropriate status
    return HttpResponse("Sadness", status_code=400)
```

操作医疗或金融数据的项目尤其需要事务功能。


## 显式事务声明

显式事务声明是提高网站性能的一种方法。即指定哪些视图或业务逻辑需要封装在事务中，哪些不需要。这种方式的缺点是增加了开发时间。

> Aymeric Augustin:
> 只要性能开销可以忍受，尽量使用 ATOMIC_REQUESTS。
> 这适合于大多数网站的情况。

何时使用事务：

+ 不进行修改的数据库操作不要封装在事务中
+ 对数据进行修改的操作应该封装在事务中
+ 即有读取，又有修改，还要考虑性能的特殊情况将影响以上这两条准则


哪些 ORM 操作应该封装在事务中：

目的     | ORM 方法                                                                     | 通常要使用事务吗？
---------|------------------------------------------------------------------------------|
创建数据 | .create(), .bulk_create(), get_or_create()                                   | 是
读取数据 | .get(), .filter(), .count(), .iterate(), exists(), .exclude(), .in_bulk() 等 | 否
修改数据 | .update()                                                                    | 是
删除数据 | .delete()                                                                    | 是


### 不能将单个 ORM 方法调用封装在事务中

为确保数据一致性，Django ORM 在进行 .create, .update(), .delete() 等涉及多条记录的操作时，实际上在内部已经使用了事务。因此不能重复使用。

## django.http.StreamingHttpResponse 和事务

此时事务只应用到视图范围，如果返回 StreamingHttpResponse 后，在开始流应答过程中出现错误，则不在事务影响范围内。因此，对于返回 StreamingHttpResponse 的视图，应该将 ATOMIC_REQUESTS 设为默认值 False，然后采用显式事务声明，或者将 **django.db.transaction.non_atomic_requests** 装饰器应用到该视图上。

## MySQL 中的事务

MySQL 是否支持事务取决于你选用哪种表类型， InnoDB 还是 MyISAM。


## Django ORM 事务相关资源

+ [Real Python 上的事务主题文章](https://realpython.com/blog/python/transaction-management-with-django-1-6/)



> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
