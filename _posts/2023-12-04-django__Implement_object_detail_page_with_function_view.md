---
title: Implement object detail page with function view
date: 2023-12-04
tags: python django views
categoris: Programming
---

1. We first create app's own urls.py and put all the paths related to the app,, see [[Define app URLs under their own path]].
2.  In app's urls.py, define a path pattern which matches the object's detail page:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/', views.detail, name='detail')
]
```

3. Define a detail view:

```python
from django.shortcuts import render, get_object_or_404
from .models import Movie

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'detail.html', { 'movie': movie })
```

4. create a template file detail.html

```html
{% extends 'base.html' %}

{% block content %}
<div>
  <div>{{ movie.title }}</div>
  <div>{{ movie.description }}</div>
</div>
{% endblock content %}
```