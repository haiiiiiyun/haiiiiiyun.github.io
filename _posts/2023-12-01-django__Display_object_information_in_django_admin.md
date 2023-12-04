---
title: Display object information in django admin
date: 2023-12-01
tags: python django admin models
categoris: Programming
---

The `__str__` method in Python represents the class object as a string. `__str__` will be called when the model objects are listed in `admin`.

If we don't define a `__str__`, model objects will be displayed as something like `Appname object(1)`.

To fix it, define `__str__` for the Model:

```python
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
	# ...

    def __str__(self):
        return self.title
```