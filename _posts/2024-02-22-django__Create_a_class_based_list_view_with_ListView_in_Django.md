---
title: Create a class based list view with ListView in Django
date: 2024-02-22
tags: python django views class-based
categoris: Programming
---

## View

```python
# views.py
from django.views.generic import ListView
from .models import Book

class BookListView(ListView):
    model = Book
    context_object_name = 'book_list' # change it from object_list to book_list in template
    template_name = 'books/book_list.html'
```

In the sub-class of `generic.ListView`, specify `model`, `template_name`.

In template, the default variable name for the object list is `object_list`,  to change it, set a value for `context_object_name` in view class.

## Template

<!-- {% raw %} -->
```html
<!-- templates/books/book_list.html -->
{% extends "_base.html" %}

{% block title %}Books{% endblock title %}

{% block content %}
    {% for book in book_list %}
        <div>
            <h2><a href="">{{ book.title }}</a></h2>
        </div>
    {% endfor %}
{% endblock content %}
```
<!-- {% endraw %} -->