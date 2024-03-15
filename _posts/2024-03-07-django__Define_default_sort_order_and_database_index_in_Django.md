---
title: Define default sort order and database index in Django
date: 2024-03-07
tags: python django models
categoris: Programming
---

## Create a default  sort order in Meta.ordering 

The default order will apply when no order is specified in the query.

## Add a database index

Define a database index for the default sort field will improve performance for queries filtering or ordering results by this field.

We add the index in Meta.indexes, a index could comprise one or multiple fields, in ascending or descending order.

```python
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']
		indexes = [
			models.Index(fields=['-publish']),
		]
    def __str__(self):
        return self.title
```
