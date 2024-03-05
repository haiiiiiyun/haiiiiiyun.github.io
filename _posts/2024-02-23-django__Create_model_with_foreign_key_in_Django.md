---
title: Create model with foreign key in Django
date: 2024-02-23
tags: python django models
categoris: Programming
---

## Model

For `ForeignKey` we must specify an `on_delete` option.

```python
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Book(models.Model):
	# ...

class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.review
```

We can set the `related_name` to make it easier to follow the foreign key relationship backwards  on queries, note this name must be unique:

```python
reviews = mybook.reviews.all();
```

## Admin

In the one-to-many relationship, we can display the reviews  as tabular inline in book:

```python
from django.contrib import admin
from .models import Book, Review

class ReviewTabularInline(admin.TabularInline):
    model = Review

class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewTabularInline
    ]
    list_display = ('title', 'author', 'price')

admin.site.register(Book, BookAdmin)
```