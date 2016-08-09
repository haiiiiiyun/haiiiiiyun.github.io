---
title: 使用 User 数据模型
date: 2016-08-09
writing-time: 2016-08-09 10:45--11:33
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 通过 Django 工具查找 User 数据模型

获取 User 类的最佳方式：

```python
# Stock user model definition
>>> from django.contrib.auth import get_user_model
>>> get_user_model()
<class 'django.contrib.auth.models.User'>

# When the project has a custom user model definition
>>> from django.contrib.auth import get_user_model
>>> get_user_model()
<class 'profiles.models.UserProfile'>
```

## 在数据模型中，使用 settings.AUTH_USER_MODEL 进行外键引用

到 User 的 ForeignKey、OneToOneKey 或 ManyToManyField 的引用方式：

```python
from django.conf import settings
from django.db import models

class IceCreamStore(models.Model):

	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=255)
```

setting.AUTH_USER_MODEL 的值一旦设置后，不要再修改，对它的修改涉及到数据库模式的大量修改！

## 到 User 的外键引用不能用 get_user_model()，会引起死循环

以下是错误的使用方法：

```python
# DON'T DO THIS!
from django.db import models
from django.contrib.auth import get_user_model

class IceCreamStore(models.Model):

	# This following line tends to create import loops.
	owner = models.OneToOneField(get_user_model())
	title = models.CharField(max_length=255)
```

## 从 1.5- 版本的 User 数据模型迁移到 1.5+ 版本

参考： [Tobias McNulty’s Tutorial](https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/) 和 [django-authtool’s Tutorial](http://django-authtools.readthedocs.io/en/latest/how-to/migrate-to-a-custom-user-model.html)


# Django 1.8 中自定义 User 项

相关包： django.authtools，其中有 AbstractEmailUser 和 AbstractNamedUser 数据模型。

## 方式 1：继承 AbstractUser

假如只需增加额外的数据项，选中该方式。这种情况下，使用 django-authtools 中的其本数据模型、表单和 admin 对象是最快最容易的实现方式，而大多数项目都符合这种情况。

示例：

```python
# profiles/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

class KarmaUser(AbstractUser):
	karma = models.PositiveIntegerField(verbose_name=_("karma"),
										default=0,
										blank=True)
```

之后，在配置文件中再进行设置：

```python
AUTH_USER_MODEL = "profiles.KarmaUser"
```

### 方式 2：继承 AbstractBaseUser

AbstractBaseUser 是基本骨架，只有 3 个项： password, last_login, is_active。如果符合以下情况，选择该方式：

+ 无需默认提供的 first_name 和 last_name 等项
+ 只想使用默认的密码处理功能

## 从相关的数据模型中进行链接

它和 1.5 版本前创建 **Profile** 数据模型的方式类似。它有以下几种使用情境：

情境 1： 创建一个第三方包

+ 该包要发布到 PyPI
+ 该包需为每个用户存储额外的信息，如 Strip ID 等

情境 2： 内部项目需求

+ 不同的用户需要不同的项
+ 该方式可以与上面的 方式 1 和方式 2 一起使用

使用这种方式，需要将不同的数据模型定义在不同的 Profile 中，如：

```python
# profiles/models.py

from django.conf import settings
from django.db import models

from flavors.models import Flavor

class EaterProfile(models.Model):

	# Default user profile
	# If you do this you need to either have a post_save signal or
	# redirect to a profile_edit view on initial login.
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	favorite_ice_cream = models.ForeignKey(Flavor, null=True, blank=True)

class ScooperProfile(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	scoops_scooped = models.IntegerField(default=0)

class InventorProfile(models.Model)

	user = models.OneToOneField(settings.AUTH_USER_MODEL) .
	flavors_invented = models.ManyToManyField(Flavor, null=True, blank=True)
```

之后，可以通过 ORM 进行访问， 如： `user.eaterprofile.favorite_ice_cream`。

注： `user.get_profile()` 已在 Django 1.7 中去除。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
