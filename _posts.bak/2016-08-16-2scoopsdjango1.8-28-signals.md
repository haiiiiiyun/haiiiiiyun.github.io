---
title: Django 的信号：安全安全和避免技术
date: 2016-08-16
writing-time: 2016-08-16 12:27--16:51
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

尽量避免使用信号。

信号是同步阻塞式的。

# 何时使用或避免使用信号

信号不适合以下情况：

+ 该信号与某个特定的数据模型相关，并且能移到数据模型的方法中，比如 save() 中
+ 该信号能用一个自定义的数据模型管理器方法来替代
+ 该信号与某个特定的视图相关，并且能移入那个视图中

以下情况可以使用信号：

+ 你的信号接收器需要对多个数据模型进行修改
+ 这个相同的信号需要在多个应用中分发，并且被一个相同的接收器处理
+ 想在数据模型保存后，用信号使缓存失效
+ 有一个需要回调的不寻常的场景，并且除了信号无法用其它方式处理。例如，想通过第三方数据模型的 save() 或 init() 来触发。

# 如何避免使用信号

## 使用自定义数据模型管理器方法来代替信号

假设 “新建” 事件需向管理员发送邮件，由管理员再进行批准。

示例如下，先创建一个数据模型管理器方法：


```python
# events/managers.py
from django.db import models

class EventManager(models.Manager):

    def create_event(self, title, start, end, creator):
        event = self.model(title=title,
                        start=start,
                        end=end,
                        creator=creator)
        event.save()
        event.notify_admins()
        return event
```

然后将其绑定到数据模型中，该模型中含 有 **notify_admins** 方法：

```python
# events/models.py
from django.conf import settings
from django.core.mail import mail_admins
from django.db import models

from model_utils.models import TimeStampedModel

from .managers import EventManager

class Event(TimeStampedModel):

    STATUS_UNREVIEWED, STATUS_REVIEWED = (0, 1)
    STATUS_CHOICES = (
        (STATUS_UNREVIEWED, "Unreviewed"),
        (STATUS_REVIEWED, "Reviewed"),
    )

    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES,
                                default=STATUS_UNREVIEWED)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = EventManager()

    def notify_admins(self):
        # create the subject and message
        subject = "{user} submitted a new event!".format(
                        user=self.creator.get_full_name())
        message = """TITLE: {title}
START: {start}
END: {end}""".format(title=self.title, start=self.start,
                    end=self.end)

        # Send to the admins!
        mail_admins(subject=subject,
                    message=message,
                    fail_silently=False)
```

然后与 **User** 的使用模式一样，创建 event 不使用 create()，而用 create_event() 方法：

```python
>>> from django.contrib.auth import get_user_model
>>> from django.utils import timezone
>>> from events.models import Event
>>> user = get_user_model().get(username="audreyr")
>>> now = timezone.now()
>>> event = Event.objects.create_event(
... title="International Ice Cream Tasting Competition",
... start=now,
... end=now,
... user=user
... )
```

## 在其它地方对数据模型进行验证

如果现在是通过 *pre_save* 信号时行验证的，可以尝试为这些数据项编写自定义的验证器。

如果是通过 **ModelForm** 进行验证，尝试覆盖数据模型的 **clean()** 方法。

## 覆盖数据模型的 save 和 delete 方法

由 **pre_save** 和 **post_save** 信号触发的逻辑可以移到数据模型的 **save()** 方法中。类似地， 由 **pre_delete** 和 **post_delete** 信号触发的可以移到 **delete()** 中。

## 使用辅助方法来替代信号

特别是在重构时，可以对这些信号进行逐渐替换。

替换的步骤：

1. 为当前的信号调用编写测试
2. 为当前的信号所调用的业务函数编写测试
3. 编写一个辅助函数来重复信号所调用的业务逻辑
4. 运行测试
5. 将信号改为调用这个辅助函数
6. 再次运行测试
7. 去除信号，直接调用该辅助函数
8. 再次运行测试


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
