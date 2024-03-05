---
title: Create a class based template view with TemplateView in Django
date: 2024-02-18
tags: python django views class-based
categoris: Programming
---

```python
# views.py
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'
```

```python
# urls.py
from django.urls import path
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]
```