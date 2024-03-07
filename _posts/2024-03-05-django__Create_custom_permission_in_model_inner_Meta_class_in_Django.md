---
title: Create custom permission in model inner Meta class in Django
date: 2024-03-05
tags: python django auth
categoris: Programming
---

`add, change, delete, view` permissions are automatically created for each model. We can refer to these permissions as:

`"{appname}.add_{modelname}"`, `"{appname}.change_{modelname}"`, `"{appname}.delete{modelname}"`, `"{appname}.view{modelname}"`.

## Create user permission

To create extra permissions, add them into model's inner `Meta` class.

```python
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='cover/', blank=True)

    class Meta:
        permissions = [
            ("special_status", "can read all books"),
        ]

    def __str__(self):
        return self.title

    # canonical URL for the model
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.pk)])
```

This is a list or tuple of 2-tuples in the format `(permission_code, human_readable_permission_name)`.

## Apply permission using PermissionRequiredMixin

`PermissionRequiredMixin` should come after `LoginRequiredMixin` but before generic view.  It requires a `permission_required` field which specifies the desired permission:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Book

class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    login_url = 'account_login'
    permission_required = 'books.special_status'
    # add multiple permissions as: permission_required = ['books.special_status',]
```