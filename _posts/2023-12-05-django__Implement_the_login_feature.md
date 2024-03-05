---
title: Implement the login feature
date: 2023-12-05
tags: python django auth
categoris: Programming
---

Similar as [[Implement a basic sign up feature]], here we use `django.contrib.auth.forms.AuthenticationForm`.

1. View:

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

def login_account(request):
    if request.method == 'GET':
        return render(request, 'accounts/login_account.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            username = request.POST['username'],
            password = request.POST['password'])
        if user is None:
            return render(request, 'accounts/login_account.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is not correct'})
        else:
            login(request, user)
            return redirect('/')
```

2. URL:

```python
urlpatterns = [
	# ...
    path('login/', views.login_account, name='login'),
]
```

3. Template:  login_account.html

See [[Implement a basic sign up feature]] and [[Customize fields of UserCreationForm]].