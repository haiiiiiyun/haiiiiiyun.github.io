---
title: Implement object listing feature with a functional view
date: 2023-11-30
tags: python django views functional templates
categoris: Programming
---

In views.py, grab model objects from DB, and pass them tin the directory to template file:

```python
from django.shortcuts import render
from .models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})
```

In template file, use `for` to loop through objects:

<!-- {% raw %} -->
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Movies App</title>
  </head>
  <body>
    <div class="container">
      {% for movie in movies %}
        <h2>{{ movie.title }}</h2>
        <h3>{{ movie.description }}</h3>
        <img src="{{ movie.image.url }}">
        {% if movie.url %}
          <a href="{{ movie.url }}">Movie Link</a>
        {% endif %}
      {% endfor %}
      <br />
      <br />
    </div>
  </body>
</html>
```
<!-- {% endraw %} -->