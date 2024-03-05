---
title: Implement a basic sign up feature
date: 2023-12-05
tags: python django auth signup
categoris: Programming
---

1. Create a dedicated app `accounts` and define , and [[Define app URLs under their own path]].

2.  URL: create a `signup` path in `accounts/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup')
]
```

3. View:  define `signup` view and pass the `UserCreationForm` as the sign up form:

```python
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    return render(request, 'accounts/signup.html', { 'form': UserCreationForm })
```

4. Template: create template `accounts/templates/accounts/signup.html` and simply render the form:

<!-- {% raw %} -->
```html
{{ form }}
```
<!-- {% endraw %} -->

5. Improve template:  make the template extend from base.html, render the fields of `form` as `<p>` and wrap them in a `form` tag and have a `submit` button:

<!-- {% raw %} -->
```html
{% extends 'base.html' %}

{% block content %}
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign up</button>
</form>
{% endblock content %}
```
<!-- {% endraw %} -->

6. Create user on submitting and handler errors:

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html', { 'form': UserCreationForm })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'accounts/signup.html', 
                    { 'form': UserCreationForm, 'error': 'Username already taken. Choose new username.'})
        else:
            return render(request, 'accounts/signup.html', 
                { 'form': UserCreationForm, 'error': 'Passwords do not match.'})
```

In template file, display the error if exists:

<!-- {% raw %} -->
```html
{% if error %}
    <div class=""alert">{{ error }}</div>
{% endif %}
```
<!-- {% endraw %} -->
