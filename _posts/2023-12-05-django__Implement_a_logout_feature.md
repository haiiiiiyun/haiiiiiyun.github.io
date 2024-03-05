---
title: Implement a logout feature
date: 2023-12-05
tags: python django auth
categoris: Programming
---

1. View:

```python
from django.contrib.auth import logout

def logout_account(request):
    logout(request)
    return redirect('/')
```

2. URL:

```python
urlpatterns = [
	# ...
    path('logout/', views.logout_account, name='logout'),
]
```

3. Template:

<!-- {% raw %} -->
```html
{% if user.is_authenticated %}
  <a class="nav-link" href="{% url 'logout' %}">Logout ({{ user.username }})</a>
{% else %}
  <a class="nav-link" href="#">Login</a>
  <a class="nav-link" href="#">Sign Up</a>
{% endif %}
```
<!-- {% endraw %} -->