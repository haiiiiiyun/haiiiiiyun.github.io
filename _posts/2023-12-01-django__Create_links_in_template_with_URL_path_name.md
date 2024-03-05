---
title: Create links in template with URL path name
date: 2023-12-01
tags: python django url templates
categoris: Programming
---

We define URL path name in `urls.py`:

```python
# …
urlpatterns = [
	path('', views.news, name='news'),
]
```

<!-- {% raw %} -->
In template file, we link it with `{% url %}` and path name:

```html
<nav>
      <a class="nav-link" href="{% url 'home' %}">Home</a>
      <a class="nav-link" href="{% url 'news' %}">News</a>
</nav>
```

If the view requires parameters, we can pass them as well:

```html
<a href="{% url 'detail' movie.id %}">{{ movie.title }}</a>
```
<!-- {% endraw %} -->