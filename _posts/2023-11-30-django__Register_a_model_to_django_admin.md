---
title: Register a model to django admin
date: 2023-11-30
tags: python django models admin
categoris: Programming
---

To add a model to admin, go to `admin.py` in an app folder, and register the model with the following:

```python
from django.contrib import admin
from .models import Movie

admin.site.register(Movie)
```