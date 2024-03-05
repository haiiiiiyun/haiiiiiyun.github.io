---
title: Create a class based detail view with DetailView in Django
date: 2024-02-22
tags: python django views class-based
categoris: Programming
---

## View

```python
# views.py
from django.views.generic import DetailView
from .models import Book

class BookDetailView(DetailView):
    model = Book
	context_object_name = 'book'
    template_name = 'books/book_detail.html'
```

In the sub-class of `generic.ListView`, specify `model`, `template_name`.

In template, the default variable name for the object list is `object`,  to change it, set a value for `context_object_name` in view class.

## Template

<!-- {% raw %} -->
```html
<!-- templates/books/book_list.html -->
{% extends "_base.html" %}

{% block title %}{{ book.title }}{% endblock title %}

{% block content %}
    <div class="book-detail">
        <h2><a href="">{{ book.title }}</a></h2>
        <p>Author: {{ book.author }}</p>
        <p>Price: {{ book.price }}</p>
    </div>
{% endblock content %}
```
<!-- {% endraw %} -->

## URLs

```python
# urls.py
from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail")
]
```

Right now the path for each object are their auto-incrementing primary key,  which is predictable, for instances:  `/books/1/`, `/books/2`,...

### get_absolute_url()

<!-- {% raw %} -->
We can reference the object's URL in template file using: `{% url 'book_detail', object.pk %}`.
<!-- {% endraw %} -->

To make it not so verbose, let's add a `get_absolute_url()` method which returns a canonical URL for the model:

```python
# models.py
from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    # canonical URL for the model
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.pk)])
```

With this update, there's no need to use the `url` template tag for the link. Instead there is one canonical reference in the model. 

<!-- {% raw %} -->
`<a href="{{ book.get_absolute_url }}">{{ book.title }}</a></h2>`
<!-- {% endraw %} -->

This is a cleaner approach and should be used whenever we need individual pages for an object.

### Replace pk with UUID

see [[Primary Keys, IDs, Slugs, UUIDs of model object in Django]].