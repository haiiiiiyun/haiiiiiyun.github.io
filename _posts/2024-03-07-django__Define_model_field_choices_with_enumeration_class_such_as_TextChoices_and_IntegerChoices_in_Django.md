---
title: Define model field choices with enumeration class such as TextChoices and IntegerChoices in Django
date: 2024-03-07
tags: python django models
categoris: Programming
---

Django provides enumeration types that we can subclass to define choices simply. See https://docs.djangoproject.com/en/4.1/ref/models/fields/#enumeration-types.

Subclass `models.TextChoices` to create choices that work with `models.TextField`, and subclass `models.IntegerChoices` to create choices that work with `models.IntegerField`.

```python
from django.db import models
from django.utils import timezone

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title
```

We can access `Post.Status.choices` to obtain the available choices, `Post.Status.labels` to obtain the hunam-readable names, and `Post.Status.valus` to obtain the actual values of the choices.

```python
(InteractiveConsole)
>>> from blog.models import Post
>>> Post.Status
<enum 'Status'>
>>> Post.Status.choices
[('DF', 'Draft'), ('PB', 'Published')]
>>> Post.Status.values
['DF', 'PB']
>>> Post.Status.names
['DRAFT', 'PUBLISHED']
>>> Post.Status.labels
['Draft', 'Published']
>>> Post.Status.DRAFT
Post.Status.DRAFT
>>> str(Post.Status.DRAFT)
'DF'
```