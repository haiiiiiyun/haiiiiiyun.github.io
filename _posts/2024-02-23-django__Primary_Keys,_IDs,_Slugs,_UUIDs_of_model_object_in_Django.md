---
title: Primary Keys, IDs, Slugs, UUIDs of model object in Django
date: 2024-02-23
tags: python django models
categoris: Programming
---

## Primary Keys vs. IDs

Django `generic.DetailView` treats them interchangeably. There is a subtle difference.

`id` is a model field automatically set by Django internally to auto-increment, such as 1, 2, 3, and so on. This is also treated as the primary key `pk` of a model.

However it's possible to manually change what the primary key is for a model. It doesn't have to be `id`.

By contrast the primary key `pk` refers to the primary key field of a model, so it's safe using `pk` even we changed the `id` of our model.


## Slugs vs. UUIDs

slug is a newspaper term for a short label for something, that is often used in URLs. There is a `SlugField` model field. The main challenge with slugs is handling duplicates.

Django supports `UUID` with a `UUIDField` model field. In production, we usually update the model's default `id` with UUID field and use it in the URL path.

### Update id with UUIDField in model

```python
import uuid
from django.db import models
from django.urls import reverse

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    # canonical URL for the model
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.pk)])
```

### replace int with uuid in urls

```python
from django.urls import path

from .views import BookListView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name="book_list"),
    path("<uuid:pk>/", BookDetailView.as_view(), name="book_detail")
]
```

### migration

The main challenge with migration is handling the existing records, the existing `id` value is not compatible with the update UUID field.

The most destructive approach is to simply delete old migrations and records and then start over.