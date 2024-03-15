---
title: default, auto_now, auto_now_add in Django DateTimeField
date: 2024-03-07
tags: python django models
categoris: Programming
---


+ published: `default`: Similar to `auto_now_add`, the current date and time will be saved as the default value when creating an object, and we can update the value in the future.
+ created: `auto_now_add`: the current date and time will be saved automatically when creating an object,  **this makes the field non-editable, we can't change the value in the future**.
+ updated: `auto_now`:  the current date and time will be saved automatically when saving an object,  **this makes the field non-editable, we can't change the value manually**.

```python
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title
```