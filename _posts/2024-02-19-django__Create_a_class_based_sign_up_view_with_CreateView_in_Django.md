---
title: Create a class based sign up view with CreateView in Django
date: 2024-02-19
tags: python django views class-based
categoris: Programming
---

Create the class based on `generic.CreateView` and specify the `form_class`, `success_url` and `template_name`.

```python
from django.views import generic
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
```