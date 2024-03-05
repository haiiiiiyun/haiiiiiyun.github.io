---
title: Define an URL and link it to a function view
date: 2023-11-16
tags: python django url
categoris: Programming
---

Remember that `/projectfolder/urls.py` is referenced each time someone types in an URL on our website.

Each time a user types in an URL, the request passes through `urls.py` and sees whether the URL matches any defined paths so the Django server can return an appropriate response.

`urls.py` has the following code by default:

```python
from django.contrib import admin
from django.urls import path
urlpatterns = [
	path('admin/', admin.site.urls),
]
```

When a request passes through `urls.py`, it will try to match a `path` object in `urlpatterns`.

## Create a view for about page in an app movie

In `movie/views.py`, add the following:

```python
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return HttpResponse('<h1>Welcome to About Page</h1>')
```

## Define a path for the about page

In `projectfoler/urls.py`, add the `import` and `path` lines:

```python
from django.contrib import admin
from django.urls import path

from movie import views as MovieViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', MovieViews.about),
]
```

Note the views are stored in the individual apps themselves such as `moview/views.py`.

To create an app, see [[Create an app in a Django project]].