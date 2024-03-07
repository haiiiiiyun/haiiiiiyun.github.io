---
title: Restrict access only to logged-in users with LoginRequiredMixin in a class based view in Django
date: 2024-03-05
tags: python django auth views class-based
categoris: Programming
---

It is important that `LoginRequiredMixin` comes before views in order to work properly. Mixins are powperful but can be tricky in pratice.

Django official docs: not all mixins can be used together, and not all generic class based views can be used with all other mixins.

`LoginRequiredMixin` requires adding a `login_url` for the user to be redirected to. This is the URL name for login.

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Book

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list' # change it from object_list to book_list in template
    template_name = 'books/book_list.html'
    login_url = 'account_login'
```